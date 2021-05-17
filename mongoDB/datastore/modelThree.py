import hashlib
import itertools
import json
import logging
import multiprocessing
import uuid
import random
from collections import OrderedDict
from datetime import datetime
from functools import partial
from logging.config import dictConfig

from bson import Code

from configs import file_path, file_name, default_offset, default_limit, mongo_server_host, mongo_ulca_m3_db
from configs import mongo_ulca_dataset_m3_col, no_of_enrich_process, no_of_dump_process

import pymongo
log = logging.getLogger('file')


mongo_instance = None

class ModelThree:
    def __init__(self):
        pass

    def load_dataset(self, request):
        log.info("Loading M3 Dataset..... | {}".format(datetime.now()))
        try:
            if 'path' not in request.keys():
                path = f'{file_path}' + f'{file_name}'
            else:
                path = request["path"]
            log.info("File -- {} | {}".format(path, datetime.now()))
            dataset = open(path, "r")
            data_json = json.load(dataset)
            if 'slice' in request.keys():
                data_json = data_json[:request["slice"]]
            total, duplicates, batch = len(data_json), 0, request["batch"]
            update_batch, update_records, insert_batch, insert_records = [], [], [], []
            log.info(f'Enriching the dataset..... | {datetime.now()}')
            func = partial(self.get_enriched_data, request=request)
            pool_enrichers = multiprocessing.Pool(no_of_enrich_process)
            enrichment_processors = pool_enrichers.map_async(func, data_json).get()
            for result in enrichment_processors:
                if result:
                    if result[1]:
                        if "INSERT" == result[1]:
                            if len(insert_batch) == batch:
                                log.info(f'Adding batch of {len(insert_batch)} to the BULK INSERT list... | {datetime.now()}')
                                insert_records.append(insert_batch)
                                insert_batch = []
                            else:
                                insert_batch.append(result[0])
                        if "UPDATE" == result[1]:
                            if len(update_batch) == batch:
                                log.info(f'Adding batch of {len(update_batch)} to the BULK UPDATE list... | {datetime.now()}')
                                update_records.append(update_batch)
                                update_batch = []
                            else:
                                update_batch.append(result[0])
                    duplicates += result[2]
            pool_enrichers.close()
            if insert_batch:
                log.info(f'Adding batch of {len(insert_batch)} to the BULK INSERT list... | {datetime.now()}')
                insert_records.append(insert_batch)
            if update_batch:
                log.info(f'Adding batch of {len(update_batch)} to the BULK UPDATE list... | {datetime.now()}')
                update_records.append(update_batch)
            pool_ins, pool_upd, ins_count, upd_count = multiprocessing.Pool(no_of_dump_process), multiprocessing.Pool(no_of_dump_process), 0, 0
            if update_records:
                log.info(f'Dumping UPDATE records.... | {datetime.now()}')
                processors = pool_upd.map_async(self.update, update_records).get()
                for result in processors:
                    upd_count += result
            pool_upd.close()
            if insert_records:
                log.info(f'Dumping INSERT records.... | {datetime.now()}')
                processors = pool_ins.map_async(self.insert, insert_records).get()
                for result in processors:
                    ins_count += result
            pool_ins.close()
            if (ins_count + upd_count) == total:
                log.info(f'Dumping COMPLETE! total: {total} | {datetime.now()}')
            log.info(f'Done! -- UPDATES: {upd_count}, INSERTS: {ins_count}, "DUPLICATES": {duplicates} | {datetime.now()}')
        except Exception as e:
            log.exception(e)
            return {"message": "EXCEPTION while loading dataset!!", "status": "FAILED"}
        return {"message": f'loaded {total} no. of records to DB', "status": "SUCCESS"}

    def get_tags(self, d):
        for v in d.values():
            if isinstance(v, dict):
                yield from self.get_tags(v)
            elif isinstance(v, list):
                for entries in v:
                    yield entries
            else:
                yield v

    def get_enriched_data(self, data, request):
        if 'sourceText' not in data.keys() or 'targetText' not in data.keys():
            return None, None, 0
        append_record = None
        src_hash = str(hashlib.sha256(data["sourceText"].encode('utf-16')).hexdigest())
        tgt_hash = str(hashlib.sha256(data["targetText"].encode('utf-16')).hexdigest())
        record = self.get_dataset_internal({"tags": [src_hash]})
        if record:
            record = record[0]
            if tgt_hash in record["tags"]:
                return None, None, 1
            else:
                append_record = record
        else:
            record = self.get_dataset_internal({"tags": [tgt_hash]})
            if record:
                append_record = record
        target = {
            "id": uuid.uuid4(),
            "targetText": data["targetText"],
            "alignmentScore": random.uniform(0, 1),
            "targetLanguage": request["details"]["targetLanguage"],
            "sourceRef": src_hash,
            "submitter": request["submitter"],
            "contributors": request["contributors"],
        }
        if 'translator' in data.keys():
            target["translator"] = data["translator"]
        if append_record:
            append_record[0]["targets"].append(target)
            tags_dict = {
                "tgtHash": tgt_hash, "lang": request["details"]["targetLanguage"],
                "collectionMode": request["details"]["collectionMode"],
                "domain": request["details"]["domain"], "licence": request["details"]["licence"]
            }
            append_record[0]["tags"].extend(list(self.get_tags(tags_dict)))
            return append_record[0], "UPDATE", 0
        else:
            targets = [target]
            tags_dict = {
                "srcHash": src_hash, "tgtHash": tgt_hash, "tgtLang": request["details"]["targetLanguage"],
                "collectionMode": request["details"]["collectionMode"], "srcLang": request["details"]["sourceLanguage"],
                "domain": request["details"]["domain"], "licence": request["details"]["licence"]
            }
            tags = list(self.get_tags(tags_dict))
            record = {
                "id": uuid.uuid4(), "sourceTextHash": src_hash, "sourceText": data["sourceText"],
                "sourceLanguage": request["details"]["sourceLanguage"],
                "submitter": request["submitter"], "contributors": request["contributors"],
                "targets": targets, "tags": tags
            }
            return record, "INSERT", 0

    def get_dataset_internal(self, query):
        try:
            db_query = {}
            if "tags" in query.keys():
                db_query["tags"] = query["tags"]
            data = self.search(db_query, True)
            if data:
                return data
            else:
                return None
        except Exception as e:
            log.exception(e)
            return None

    def get_dataset(self, query):
        log.info(f'Fetching datasets..... | {datetime.now()}')
        try:
            db_query = {}
            tags = []
            if 'srcLang' in query.keys():
                tags.append(query["srcLang"])
                db_query["srcLang"] = query["srcLang"]
            if 'tgtLang' in query.keys():
                for tgt in query["tgtLang"]:
                    tags.append(tgt)
                db_query["tgtLang"] = query["tgtLang"]
            if 'collectionMode' in query.keys():
                tags.append(query["collectionMode"])
            if 'licence' in query.keys():
                tags.append(query["licence"])
            if 'domain' in query.keys():
                tags.append(query["domain"])
            if tags:
                db_query["tags"] = tags
            data = self.search(db_query, False)
            count = len(data)
            if count > 30:
                data = data[:30]
            log.info(f'Result count: {count} | {datetime.now()}')
            log.info(f'Done! | {datetime.now()}')
            return {"count": count, "query": db_query, "dataset": data}
        except Exception as e:
            log.exception(e)
            return {"message": str(e), "status": "FAILED", "dataset": "NA"}

    ####################### DB ##############################

    def set_mongo_cluster(self, create):
        if create:
            log.info(f'Setting the Mongo Shard Cluster up..... | {datetime.now()}')
            client = pymongo.MongoClient(mongo_server_host)
            client.drop_database(mongo_ulca_m3_db)
            ulca_db = client[mongo_ulca_m3_db]
            ulca_col = ulca_db[mongo_ulca_dataset_m3_col]
            ulca_col.create_index([("data.score", -1)])
            ulca_col.create_index([("tags", -1)])
            db = client.admin
            db.command('enableSharding', mongo_ulca_m3_db)
            key = OrderedDict([("_id", "hashed")])
            db.command({'shardCollection': f'{mongo_ulca_m3_db}.{mongo_ulca_dataset_m3_col}', 'key': key})
            log.info(f'Done! | {datetime.now()}')
        else:
            return None

    def instantiate(self):
        client = pymongo.MongoClient(mongo_server_host)
        db = client[mongo_ulca_m3_db]
        mongo_instance = db[mongo_ulca_dataset_m3_col]
        return mongo_instance

    def get_mongo_instance(self):
        if not mongo_instance:
            return self.instantiate()
        else:
            return mongo_instance

    def insert(self, data):
        col = self.get_mongo_instance()
        col.insert_many(data)
        return len(data)

    def update(self, data):
        col = self.get_mongo_instance()
        bulk = col.initialize_unordered_bulk_op()
        for record in data:
            bulk.find({'id': record["id"]}).update({'$set': {'targets': record["targets"], "tags": record["tags"]}})
        bulk.execute()
        return len(data)

    # Searches the object into mongo collection
    def search(self, query, internal):
        result = []
        try:
            col = self.get_mongo_instance()
            pipeline = []
            if "tags" in query.keys():
                if internal:
                    pipeline.append({"$match": {"tags": {"$in": query["tags"]}}})
                else:
                    pipeline.append({"$match": {"tags": {"$all": query["tags"]}}})
            if 'srcLang' in query.keys() and 'tgtLang' in query.keys():
                pipeline.append({"$unwind": "$targets"})
                pipeline.append({"$match": {"$or": [{"sourceLanguage": query["tgtLang"]}, {"targets.targetLanguage": query["tgtLang"]}]}})
                pipeline.append({"$match": {"$or": [{"sourceLanguage": query["srcLang"]}, {"targets.targetLanguage": query["srcLang"]}]}})
            elif 'srcLang' in query.keys():
                pipeline.append({"$unwind": "$targets"})
                pipeline.append({"$match": {"$or": [{"sourceLanguage": query["srcLang"]}, {"targets.targetLanguage": query["srcLang"]}]}})
            if 'groupBySource' in query.keys():
                pipeline.append({"$group": {"_id": {"sourceHash": "$srcHash"}, "count": {"$sum": {"$cond": [{"$gt": ["$targets", query["countOfTranslations"]]}, 1, 0]}}}})
                if 'countOfTranslations' in query.keys():
                    pipeline.append({"$group": {"_id": {"sourceHash": "$srcHash"}, "count": {
                        "$sum": {"$cond": [{"$gt": ["$targets", query["countOfTranslations"]]}, 1, 0]}}}})
                else:
                    pipeline.append({"$group": {"_id": {"sourceHash": "$srcHash"}, "count": {"$sum": {"$cond": [{"$gt": ["$targets", 1]}, 1, 0]}}}})
            pipeline.append({"$project": {"_id": 0}})
            res = col.aggregate(pipeline, allowDiskUse=True)
            if res:
                for record in res:
                    result.append(record)
            if 'srcLang' in query.keys() and 'tgtLang' in query.keys():
                result = self.post_process(query, result)
        except Exception as e:
            log.exception(e)
        return result

    def post_process(self, query, res):
        src_lang, tgt_lang = None, None
        if 'srcLang' in query.keys():
            src_lang = query["srcLang"]
        if 'tgtLang' in query.keys():
            tgt_lang = query["tgtLang"]
        result_set = []
        for record in res:
            result_array = []
            result = {}
            if src_lang == result["sourceLanguage"]:
                result["sourceText"] = record["sourceText"]
            elif tgt_lang == result["sourceLanguage"]:
                result["targetText"] = record["targetText"]
            if result:
                for target in record["targets"]:
                    if 'sourceText' in result.keys():
                        if tgt_lang == target["targetLanguage"]:
                            result["targetText"] = target["targetText"]
                            result_array.append(result)
                    elif 'targetText' in result.keys():
                        if tgt_lang == target["sourceLanguage"]:
                            result["sourceText"] = target["targetText"]
                            result_array.append(result)
            else:
                target_combinations = list(itertools.combinations(record["targets"], 2))
                for combination in target_combinations:
                    if src_lang == combination[0]["targetLanguage"]:
                        result["sourceText"] = combination[0]["targetText"]
                    elif tgt_lang == combination[0]["targetLanguage"]:
                        result["targetText"] = combination[0]["targetText"]
                    if result:
                        if src_lang == combination[1]["targetLanguage"]:
                            result["sourceText"] = combination[1]["targetText"]
                        elif tgt_lang == combination[1]["targetLanguage"]:
                            result["targetText"] = combination[1]["targetText"]
                        if len(result.keys()) == 2:
                            result_array.append(result)
                        else:
                            result = {}
                            continue
                    else:
                        continue
            result_set.append(result_array)
        return result_set


# Log config
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] {%(filename)s:%(lineno)d} %(threadName)s %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'info': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': 'info.log'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        'file': {
            'level': 'DEBUG',
            'handlers': ['info', 'console'],
            'propagate': ''
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['info', 'console']
    }
})
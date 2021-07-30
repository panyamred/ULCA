const endpoints = {

  getContributionList: '/ulca/apis/v0/dataset/listByUserId',
  getDetailReport: '/ulca/apis/v0/dataset/getByServiceRequestNumber',
  dataSetSearchApi: '/ulca/data-metric/v0/store/search',
  login: '/ulca/user-mgmt/v1/users/login',
  datasetSubmit: '/ulca/apis/v0/dataset/corpus/submit',
  getSearchOptions: '/ulca/user-mgmt/v1/users/login',
  mySearches: "/ulca/apis/v0/dataset/corpus/search/listByUserId",
  submitSearchReq: '/ulca/apis/v0/dataset/corpus/search',
  errorReport: '/ulca/error-consumer/v0/error/report',
  register: "/ulca/user-mgmt/v1/users/signup",
  activateUser: "/ulca/user-mgmt/v1/users/verify-user",
  forgotPassword: "/ulca/user-mgmt/v1/users/forgot-password",
  tokenSearch: '/ulca/user-mgmt/v1/users/get/token/status',
  resetPassword: '/ulca/user-mgmt/v1/users/reset-password',
  modelSubmit: '/ulca/apis/v0/dataset/corpus/submit',
  modelSearch: '/ulca/apis/v0/model/search',
  getModelContributionList :"/ulca/apis/v0/model/listByUserId"
};

export default endpoints;

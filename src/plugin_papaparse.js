import papa from 'papaparse'

export default {
    install: function(app,) {
        app.config.globalProperties.$papa = papa;
    }
  }
import tesseract from 'tesseract.js'

export default {
    install: function(app,) {
        app.config.globalProperties.$tesseract = tesseract;
    }
  }
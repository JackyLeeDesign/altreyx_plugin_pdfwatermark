<template>

  <div class="container-fluid">
    <!-- PwC logo -->
    <div class="row">
      <div class="col">
        <div style="margin-top:20px;">
          <img src="./PwC.png" style="width: 100px;">
        </div>
      </div>
    </div>

    <!-- 主要內容 -->
    <div class="row">
      <div class="col">
        <!-- 第一步 -->
        <div class="card" style="margin-top:10px;">
          <div class="card-header d-flex justify-content-between align-items-center"><b>請選擇欲合併的PDF檔所在資料夾：</b></div>
          <div class="card-body" style="overflow-x:auto;">
            <label for="exampleFormControlInput1" class="form-label"><b>
                <BIconFiles style="vertical-align:text-top;" class="icon" />本元件將指定資料夾內所有PDF檔進行合併。
              </b></label>
            <ayx data-ui-props='{type:"FileBrowse", widgetId:"pdf_dir", browseType:"Folder"}'></ayx>
          </div>
        </div>

        <!-- 第二步 -->
        <!-- <div class="card" style="margin-top:10px;">
          <div class="card-header d-flex justify-content-between align-items-center"><b>Step3：請選擇待處理頁數</b></div>
          <div class="card-body" style="overflow-x:auto;">
            <div class="form-check mb-3">
              <input type="checkbox" class="form-check-input" v-model="pdf_isToDoAll" />
              <label for="exampleFormControlInput1" class="form-check-label"><b>
                  處理所有頁數
                </b></label>
            </div>
            <div class="mb-3" v-if="pdf_isToDoAll === false">
              <label for="exampleFormControlInput1" class="form-label"><b>
                  <BIconColumns style="vertical-align:text-top;" class="icon" /> 跨頁數請用","分隔，如:1,3,5。 某範圍頁數可用 "-"
                  表示，如:1-3。
                  亦可搭配使用，如:1-3,5,7
                </b></label>
              <input type="text" id="exampleFormControlInput1" class="form-control" placeholder="輸入頁數"
                v-model="pdf_page">
            </div>
          </div>
        </div> -->

      </div>
    </div>
  </div>

  <footer class="footer mt-auto">
    <p class="text-muted" style="margin: 0px;text-align: center;">版本：0.0.1</p>
  </footer>

</template>
<script>

//replaceAll Polyfill

/**
 * String.prototype.replaceAll() polyfill
 * https://gomakethings.com/how-to-replace-a-section-of-a-string-with-another-one-with-vanilla-js/
 * @author Chris Ferdinandi
 * @license MIT
 */
if (!String.prototype.replaceAll) {
  String.prototype.replaceAll = function (str, newStr) {

    // If a regex pattern
    if (Object.prototype.toString.call(str).toLowerCase() === '[object regexp]') {
      return this.replace(str, newStr);
    }

    // If a string
    return this.replace(new RegExp(str, 'g'), newStr);

  };
}

//Clean Punctuation
String.prototype.clsPunc = function () {
  return this.replace(/[\p{P}\p{S}\p{Z}]/gu, '').toLowerCase()
}


export default {
  name: 'files',
  data() {
    return {
    }
  },
  components: {
  },
  watch: {
  },
  mounted() {
    if (typeof window.Alteryx !== 'undefined') {
      //Load Alteryx Library
      document.write('<link rel="import" href="' + window.Alteryx.LibDir + '2/lib/includes.html">');
      let libpath = window.Alteryx.LibDir + "2/lib/build/designerDesktop.bundle.js"
      let script = document.createElement('script')
      script.setAttribute('src', libpath)
      //Script Onload Callback
      script.onload = function () {
        //Define DataItem
        window.Alteryx.Gui.BeforeLoad = function (manager, AlteryxDataItems) {
          var pdf_dir = new AlteryxDataItems.SimpleString('pdf_dir')
          manager.addDataItem(pdf_dir)
          // Bind to Checkbox widget
          manager.bindDataItemToWidget(pdf_dir, 'pdf_dir')
        }

        //Load Settings
        // window.Alteryx.Gui.AfterLoad = function (manager) {
        //   this.rotate_angle = manager.getDataItem("rotate_angle").getValue()
        //   this.pdf_page = manager.getDataItem("pdf_page").getValue()
        //   this.pdf_dir = manager.getDataItem("pdf_dir").getValue()
        // }.bind(this)
      }.bind(this)
      //Load Script
      document.head.appendChild(script)
    }
  },
  computed: {
  },
  methods: {
  }
}
</script>

<style>
#app {
  font-family: "Helvetica Neue", Helvetica, Arial, "Microsoft JhengHei", "PingFang TC", "Heiti TC", sans-serif;
  display: flex;
  flex-direction: column;
  height: 100%;
}

html,
body {
  height: 100%;
}
</style>

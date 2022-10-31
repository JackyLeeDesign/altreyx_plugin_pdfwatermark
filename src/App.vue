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
          <div class="card-header d-flex justify-content-between align-items-center"><b>Step1：請選擇欲添加浮水印的PDF檔</b></div>
          <div class="card-body" style="overflow-x:auto;">
            <label for="exampleFormControlInput1" class="form-label"><b>
                <BIconFiles style="vertical-align:text-top;" class="icon" />本元件將指定PDF檔添加浮水印。
              </b></label>
            <button type="button" class="btn" style="padding:0px;" v-on:click="help_1 = !help_1">
              <span v-if="!help_1">
                <BIconEyeFill style="vertical-align:text-top;" class="icon" /> 檢視教學
              </span>
              <span v-if="help_1">
                <BIconEyeSlashFill style="vertical-align:text-top;" class="icon" /> 隱藏教學
              </span>
            </button>
            <br>
            <div v-if="help_1">
              <div class="mb-3" style="display:grid;justify-content:space-around;">
                <label class="form-label"><b>1.可於元件前連結其他元件或直接選擇PDF檔案，若您是直接選擇PDF檔案則可跳過2~3步驟。</b></label>
                <img src="./step_1_1.png" style="width: 100%;max-width:650px;">
              </div>
              <div class="mb-3" style="display:grid;justify-content:space-around;">
                <label
                  class="form-label"><b>2.連結輸入資料後，因資料可能包含多個欄位，確認"檔案路徑"欄位。(下圖以資料夾工具為範例，其輸出結果有許多欄位，但只有路徑欄位才是我們需要的，故此處我們選擇
                    fullpath 完整路徑欄位，提供後續轉置元件處理)</b></label>
                <img src="./step_1_2.png" style="width: 100%;max-width:650px;">
              </div>
              <div class="mb-3" style="display:grid;justify-content:space-around;">
                <label class="form-label"><b>3.選擇欄位。</b></label>
                <img src="./step_1_3.png" style="width: 100%;max-width:650px;">
              </div>
              <div class="mb-3" style="display:grid;justify-content:space-around;">
                <label class="form-label"><b>若前面接的是PDF合併元件或PDF轉置元件，按同樣邏輯，我們選擇路徑欄位 Output Path 即可。</b></label>
                <img src="./step_1_4.png" style="width: 100%;max-width:650px;">
              </div>
            </div>
            <ayx v-if="input_isConnectFile !== true"
              data-ui-props='{type:"FileBrowse", widgetId:"pdf_path", browseType:"File", fileTypeFilters: "PDF Files (*.pdf)|*.pdf"}'>
            </ayx>
            <div class="mb-3">
              <label v-if="input_isConnectFile === true" for="exampleFormControlInput1" class="form-label"><b>
                  <BIconColumns style="vertical-align:text-top;" class="icon" />根據您所連接的檔案，請選擇其路徑欄位
                </b></label>
              <select v-if="input_isConnectFile === true" class="form-control" v-model="connectInputPathMapping">
                <option disabled value="">選擇欄位</option>
                <option v-for="item, index in str_columns" v-bind:key="index">{{ item }}</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 第二步 -->
        <div class="card" style="margin-top:10px;">
          <div class="card-header d-flex justify-content-between align-items-center"><b>Step2：請輸入浮水印提示訊息</b></div>
          <div class="card-body" style="overflow-x:auto;">
            <label for="exampleFormControlInput1" class="form-label"><b>
                <BIconColumns style="vertical-align:text-top;" class="icon" /> 此內容將顯示於每一頁頂部提示訊息框，當前日期則使用"＠"代替。
                <div class="mt-3">此欄位不得為空，預設內容為 ：</div>
                <div>"<span style="color:orangered;">本資料係稿本@，僅供參考，不得移作其他用途。</span>"</div>
                <div>呈限於頂部提示框內容如下</div>
                <img src="./step_2_1.png" style="width: 80%;max-width:650px;">
                <!-- "<span style="color:orangered">本資料係稿本 (YYYY.MM.DD hh:mm:ss) ，僅供參考，不得移作其他用途。</span>" -->
              </b></label>
            <input type="text" id="exampleFormControlInput1" class="form-control" placeholder="輸入提示訊息"
              v-model="input_annot">
          </div>
        </div>
      </div>
    </div>
  </div>

  <footer class="footer mt-auto">
    <p class="text-muted" style="margin: 0px;text-align: center;">版本：0.1.0</p>
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
      connectInputPathMapping: "",
      input_isConnectFile: false,
      pdf_path: "",
      input_annot: "",
      str_columns: [],
      val_columns: [],
      help_1: false
    }
  },
  components: {
  },
  watch: {
    input_isConnectFile: {
      handler(val) {
        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("input_isConnectFile").setValue(val)
        }
      },
      deep: true
    },
    connectInputPathMapping: {
      handler(val) {
        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("connectInputPathMapping").setValue(val)
        }
      },
      deep: true
    },
    input_annot: {
      handler(val) {
        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("input_annot").setValue(val)
        }
      },
      deep: true
    },
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
          var input_annot = new AlteryxDataItems.SimpleString('input_annot')
          manager.addDataItem(input_annot)
          var connectInputPathMapping = new AlteryxDataItems.SimpleString('connectInputPathMapping')
          manager.addDataItem(connectInputPathMapping)
          var input_isConnectFile = new AlteryxDataItems.SimpleBool('input_isConnectFile')
          manager.addDataItem(input_isConnectFile)
          var pdf_path = new AlteryxDataItems.SimpleString('pdf_path')
          manager.addDataItem(pdf_path)
          manager.bindDataItemToWidget(pdf_path, 'pdf_path')
          
          manager.getDataItem('input_annot').setValue("本資料係稿本@，僅供參考，不得移作其他用途。")
        }
        //Load Settings
        window.Alteryx.Gui.AfterLoad = function (manager) {
          //Set WorkflowDirectory
          let altreyx_input_annot = manager.getDataItem('input_annot').getValue()
          if(!altreyx_input_annot){
            this.input_annot = "本資料係稿本@，僅供參考，不得移作其他用途。"
          }else {
            this.input_annot = manager.getDataItem("input_annot").getValue()
          }
          // this.pdf_page = manager.getDataItem("pdf_page").getValue()
          // this.pdf_isToDoAll = manager.getDataItem("pdf_isToDoAll").getValue()
          this.connectInputPathMapping = manager.getDataItem("connectInputPathMapping").getValue()
          this.input_isConnectFile = manager.getDataItem("input_isConnectFile").getValue()

          // Load Income Field
          let str_type = ["String", "WString", "V_String", "V_WString", "Date", "Time", "DateTime"]
          let val_type = ["Byte", "Int16", "Int32", "Int64", "FixedDecimal", "Float", "Double"]
          let incomingFields = manager.getIncomingFields()
          this.str_columns = incomingFields.filter(item => str_type.indexOf(item.strType) > -1).map(item => item.strName)
          this.val_columns = incomingFields.filter(item => val_type.indexOf(item.strType) > -1).map(item => item.strName)

          if ((this.str_columns.length + this.val_columns.length) === 0) {
            this.input_isConnectFile = false;
          }
          else {
            this.input_isConnectFile = true;
          }
        }.bind(this)
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

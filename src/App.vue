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
          <div class="card-header d-flex justify-content-between align-items-center"><b>Step1 : 請選擇欲添加浮水印之 PDF 檔</b>
          </div>
          <div class="card-body" style="overflow-x:auto;">
            <label for="exampleFormControlInput1" class="form-label"><b>
                <BIconFiles style="vertical-align:text-top;" class="icon" />本元件會依據您的設定，於 PDF 檔中添加浮水印
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
                <label class="form-label"><b>1-1 可於元件前連結其他元件（例如 : Directory ) 或直接選擇 PDF 檔案 ;<br>若直接選擇 PDF 檔案，請跳過 1-1 及
                    1-2 步驟</b></label>
                <img src="./step_1_1.png" style="width: 100%;max-width:650px;">
              </div>
              <div class="mb-3" style="display:grid;justify-content:space-around;">
                <label class="form-label"><b>1-2 請確認輸入元件之"檔案路徑" 欄位 :<br>（下圖以Directory為例，請選擇 "FullPath" 完整路徑欄位，提供元件後續使用）</b></label>
                <img src="./step_1_2.png" style="width: 100%;max-width:650px;">
              </div>
              <div class="mb-3" style="display:grid;justify-content:space-around;">
                <label class="form-label"><b>1-3 請選擇 "檔案路徑" 欄位 </b></label>
                <img src="./step_1_3.png" style="width: 100%;max-width:650px;">
              </div>
              <div class="mb-3" style="display:grid;justify-content:space-around;">
                <label class="form-label"><b>若前面接的是 PDF 合併元件或 PDF 轉置元件，請選擇 "Output Path" 路徑欄位</b></label>
                <img src="./step_1_4.png" style="width: 100%;max-width:650px;">
              </div>
            </div>
            <ayx v-if="input_isConnectFile !== true"
              data-ui-props='{type:"FileBrowse", widgetId:"pdf_path", browseType:"File", fileTypeFilters: "PDF Files (*.pdf)|*.pdf"}'>
            </ayx>
            <div class="mb-3">
              <label v-if="input_isConnectFile === true" for="exampleFormControlInput1" class="form-label"><b>
                  <BIconColumns style="vertical-align:text-top;" class="icon" />請依據您所連結之輸入元件，選擇 "檔案路徑" 欄位
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
          <div class="card-header d-flex justify-content-between align-items-center"><b>Step2 : 請輸入浮水印提示訊息 </b></div>
          <div class="card-body" style="overflow-x:auto;">
            <div class="form-check form-check-inline mb-2">
              <input type="checkbox" class="form-check-input" v-model="input_isNeedAnnot" />
              <label for="exampleFormControlInput3" class="form-check-label"><b>
                  添加頂部訊息
                </b></label>
            </div>
            <div v-if="input_isNeedAnnot.toString() == 'true'" class="mb-3">
              <div>
                <BIconColumns style="vertical-align:text-top;" class="icon" /> 頂部訊息
              </div>
              <label for="exampleFormControlInput1" class="form-label"><b>
                  <div>此訊息將顯示於每一頁頂部，欲顯示目前日期請使用"@"代替</div>
                  <div class="mt-2">預設訊息為 :</div>
                  <div>"<span style="color:orangered;">＂本資料係稿本＠，僅供參考，不得移作其他用途</span>"</div>
                  <div>呈現於頂部訊息如下 :</div>
                  <img src="./step_2_1.png" style="width: 80%;max-width:650px;">
                </b></label>
              <input type="text" id="exampleFormControlInput1" class="form-control" placeholder="輸入提示訊息"
                v-model="input_annot">
            </div>
            <div>
              <div class="form-check form-check-inline mb-2">
                <input type="checkbox" class="form-check-input" v-model="input_isNeedWatermark" />
                <label for="exampleFormControlInput3" class="form-check-label"><b>
                  添加 "DRAFT" 字樣浮水印
                  </b></label>
              </div>
              <div v-if="input_isNeedWatermark.toString() == 'true'">
                <div>PDF 頁面中間處添加 "DRAFT" 字樣浮水印，如下圖所示 : </div>
                <img src="./step_2_2.png" style="width: 80%;max-width:650px;">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <footer class="footer mt-auto">
    <p class="text-muted" style="margin: 0px;text-align: center;">版本：0.1.7</p>
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
      help_1: false,
      input_isNeedAnnot: "",
      input_isNeedWatermark:"",
      last_incoming_fields:""
    }
  },
  components: {
  },
  watch: {
    last_incoming_fields:{
      handler(val) {
        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("last_incoming_fields").setValue(val)
        }
      },
      deep: true
    },
    input_isNeedAnnot: {
      handler(val) {
        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("input_isNeedAnnot").setValue(val)
        }
      },
      deep: true
    },
    input_isNeedWatermark:{
      handler(val) {
        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("input_isNeedWatermark").setValue(val)
        }
      },
      deep: true
    },
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
          var input_isNeedAnnot = new AlteryxDataItems.SimpleString('input_isNeedAnnot')
          manager.addDataItem(input_isNeedAnnot)
          var input_isNeedWatermark = new AlteryxDataItems.SimpleString('input_isNeedWatermark')
          manager.addDataItem(input_isNeedWatermark)
          var last_incoming_fields = new AlteryxDataItems.SimpleString('last_incoming_fields')
          manager.addDataItem(last_incoming_fields)
          var pdf_path = new AlteryxDataItems.SimpleString('pdf_path')
          manager.addDataItem(pdf_path)
          manager.bindDataItemToWidget(pdf_path, 'pdf_path')

          manager.getDataItem('input_annot').setValue("本資料係稿本@，僅供參考，不得移作其他用途。")
        }
        //Load Settings
        window.Alteryx.Gui.AfterLoad = function (manager) {
          //Set WorkflowDirectory
          let altreyx_input_annot = manager.getDataItem('input_annot').getValue()
          if (!altreyx_input_annot) {
            this.input_annot = "本資料係稿本@，僅供參考，不得移作其他用途。"
          } else {
            this.input_annot = manager.getDataItem("input_annot").getValue()
          }
          // this.pdf_page = manager.getDataItem("pdf_page").getValue()
          // this.pdf_isToDoAll = manager.getDataItem("pdf_isToDoAll").getValue()
          this.connectInputPathMapping = manager.getDataItem("connectInputPathMapping").getValue()
          this.input_isConnectFile = manager.getDataItem("input_isConnectFile").getValue()
          this.input_isNeedAnnot = manager.getDataItem("input_isNeedAnnot").getValue()
          this.input_isNeedWatermark = manager.getDataItem("input_isNeedWatermark").getValue()
          this.last_incoming_fields = manager.getDataItem("last_incoming_fields").getValue()

          // Load Income Field
          let str_type = ["String", "WString", "V_String", "V_WString", "Date", "Time", "DateTime"]
          let val_type = ["Byte", "Int16", "Int32", "Int64", "FixedDecimal", "Float", "Double"]
          let incomingFields = manager.getIncomingFields()
          this.str_columns = incomingFields.filter(item => str_type.indexOf(item.strType) > -1).map(item => item.strName)
          this.val_columns = incomingFields.filter(item => val_type.indexOf(item.strType) > -1).map(item => item.strName)
          // 若有更換連結檔案,則需自動抓取 Mapping 欄位
          if (JSON.stringify(incomingFields) !== this.last_incoming_fields) {
            if (this.str_columns.includes("FullPath")) {
              this.connectInputPathMapping = "FullPath"
            }
            else if (this.str_columns.includes("Output Path")) {
              this.connectInputPathMapping = "Output Path"
            }
            else {
              this.connectInputPathMapping = ""
            }
          }
          // 上次連結欄位
          this.last_incoming_fields = JSON.stringify(incomingFields)
          if (this.input_isNeedAnnot === "") {
            this.input_isNeedAnnot = true
          }
          if(this.input_isNeedWatermark === ""){
            this.input_isNeedWatermark = true
          }
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

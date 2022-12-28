# List all non-standard packages to be imported by your 
# script here (only missing packages will be installed)
from ayx import Package
try:
    Package.installPackages(package=['pandas','pymupdf==1.21.0'], install_type="install --user")
except:
    pass
# -----------------------
from ayx import Alteryx
from datetime import datetime
import pandas as pd
import os
import fitz
from PIL import Image
input_data = Alteryx.read("#1")
try:
    pdf_result=""
    # 讀取參數設定
    input_isConnectFile = input_data['input_isConnectFile'].iloc[0]
    if (input_isConnectFile==True):
        pdf_list = input_data['connect_input_path']
    else:
        pdf_list = input_data['pwc_input_path']
    annot_list = input_data['input_annot']
    watermark_pic_path = input_data['input_watermark'].iloc[0]
    isNeedAnnot = input_data['input_isNeedAnnot'].iloc[0]
    isNeedWatermark = input_data['input_isNeedWatermark'].iloc[0]
    # 宣告輸出結果之pandas表格
    resultTemplate = {
        "Source File": pdf_list,
        "Status":"",
        "Message":"",
        "Output Path":""
    }
    resultData = pd.DataFrame(resultTemplate)
    for index_file in range(len(pdf_list)):
        try:
            pdf_result=""
            content_pdf = pdf_list[index_file]
            # 檔案若存在則合併,反之則標示錯誤並顯示錯誤訊息
            isExist = os.path.exists(content_pdf)
            if(isExist == True):
                # 輸出結果之檔名判斷，若已存在則補序號
                file = os.path.splitext(content_pdf)[0]
                ext = os.path.splitext(content_pdf)[1]
                if(ext != ".pdf"):
                    # raise Exception("該檔案非 PDF 檔，故不處理 ! ")
                    continue
                pdf_result=f'{file}_watermark{ext}'
                i = 2
                while os.path.exists(pdf_result):
                    pdf_result = f'{file}_watermark({i}){ext}'
                    i += 1
                # 添加浮水印
                # 是否處理所有頁數，目前預設為"是"
                page_indices= "ALL"
                # reader = PdfReader(content_pdf)
                if page_indices == "ALL":

                    # 接著開始處理文件頭提示
                    black  = (0,0,0)
                    # 字段切割處理
                    strContent = annot_list[index_file]
                    strContentSplit = strContent.split("@")
                    isContainDate = '@' in strContent
                    strPart1=""
                    strPart2=""
                    if(len(strContentSplit)>=2):
                        strPart1=strContentSplit[0]
                        strPart2=strContentSplit[1]
                    if(len(strContentSplit)==1):
                        strPart1=strContentSplit[0]

                    # 獲取當前日期
                    currentDateAndTime = datetime.now()
                    year = str(currentDateAndTime.year)
                    month = str(currentDateAndTime.month)
                    day = str(currentDateAndTime.day)
                    hour = str(currentDateAndTime.hour)
                    minute = str(currentDateAndTime.minute)
                    second = str(currentDateAndTime.second)
                    strTime="(" + year + "." + month + "." + day + " " + hour + ":" + minute + ":" + second + ")"

                    pdfDoc = fitz.open(content_pdf)
                    for page in pdfDoc:
                        # 獲取當前頁面旋轉角度
                        currentRotation = page.rotation
                        page.clean_contents()
                        # 獲取原頁面高度與寬度(未轉置前)
                        page.set_rotation(0)
                         # 寬度
                        ori_width = page.rect.x1
                        # 高度
                        ori_height = page.rect.y1

                        # 獲取調整計算文件寬度與高度
                        if(currentRotation == 0 or currentRotation == 180):
                            # 寬度
                            rotated_width = ori_width 
                            # 高度
                            rotated_height = ori_height

                        if(currentRotation == 90 or currentRotation == 270):
                            # 寬度
                            rotated_width = ori_height
                            # 高度
                            rotated_height = ori_width
                        page.set_rotation(currentRotation)

                        # 提示字段Part1寬度
                        strPart1_width = len(strPart1)*8
                        # 提示字段Part2寬度
                        strPart2_width = len(strPart2)*8
                        # 時間字段寬度
                        strTime_width = len(strTime)*5
                        # 提示字段總寬度(已含框線與字的間距)
                        total_str_width = strPart1_width 
                        if(isContainDate):
                            total_str_width += strTime_width
                        if(strPart2!=""):
                            total_str_width += strPart2_width

                        # 字段之間的間距
                        rect_margin = 5
                        # 框線與字的間距
                        rect_border_margin = 8
                        # 文字框高度
                        rect_height = 8
                        # 文字框距離文件上方高度
                        rect_top = 20

                        # 浮水印
                        # 獲取浮水印圖片寬度與高度
                        # with Image.open(watermark_pic_path) as image:
                        #     watermark_pic_width, watermark_pic_height = image.size
                        # print(watermark_pic_width)
                        # print(watermark_pic_height)
                        # 浮水印寬度
                        watermark_width = 360
                        # 浮水印高度
                        watermark_height = 72
                    
                        adjustTextRotation = 0
                        adjustRotation = 0
                        # 最大可填字數計算
                        # print((total_width-strTime_width-rect_border_margin*2-rect_margin*4)/8)
                        if (currentRotation==0):
                            # 頂部提示框起點
                            rect_border_x1 = (rotated_width - total_str_width)/2 - rect_border_margin
                            rect_border_y1 = rect_top
                            # 頂部提示框結束點
                            rect_border_x2 = rect_border_x1 + total_str_width + rect_border_margin * 2
                            rect_border_y2 = rect_border_y1 + rect_height + rect_border_margin * 2
                            # 頂部提示框文字與時間位置
                            textPos1 = fitz.Point(rect_border_x1 + rect_border_margin, rect_border_y1 + 14) 
                            timePos = fitz.Point(textPos1.x + strPart1_width , textPos1.y)
                            textPos2 = fitz.Point(timePos.x + strTime_width,textPos1.y)

                            # 浮水印起點
                            watermark_x1 = (rotated_width-watermark_width)/2
                            watermark_y1 = (rotated_height-watermark_height)/2
                            # 浮水印結束點
                            watermark_x2 = watermark_x1 + watermark_width
                            watermark_y2 = watermark_y1 + watermark_height

                        if (currentRotation==90):
                            # 頂部提示起點
                            rect_border_x1 = rect_top
                            rect_border_y1 = (rotated_width - total_str_width)/2
                            # 頂部提示結束點
                            rect_border_x2 = rect_top + rect_height + rect_border_margin * 2
                            rect_border_y2 = (rotated_width - total_str_width)/2 + total_str_width + rect_border_margin * 2
                            # 頂部提示框文字與時間位置
                            textPos1 = fitz.Point(rect_border_x1 + 14,rect_border_y2 - rect_border_margin)
                            timePos = fitz.Point(textPos1.x, textPos1.y - strPart1_width)
                            textPos2 = fitz.Point(textPos1.x,timePos.y - strTime_width)
                            # 計算頂部提示內容調整角度    
                            adjustTextRotation = 90

                            # 浮水印起點
                            watermark_x1 = (ori_width-watermark_height)/2
                            watermark_y1 = (ori_height-watermark_width)/2
                            # 浮水印結束點
                            watermark_x2 = watermark_x1 + watermark_height
                            watermark_y2 = watermark_y1 + watermark_width
                            # 計算浮水印調整角度    
                            adjustRotation = 90

                        if (currentRotation==180):
                            # 頂部提示起點
                            rect_border_x1 = (rotated_width - total_str_width)/2
                            rect_border_y1 = ori_height - rect_top - rect_height - rect_border_margin*2
                            # 頂部提示結束點
                            rect_border_x2 = (rotated_width - total_str_width)/2 + total_str_width + rect_border_margin * 2
                            rect_border_y2 = ori_height - rect_top
                             # 頂部提示框文字與時間位置
                            textPos1 = fitz.Point(rect_border_x2 - rect_border_margin, rect_border_y2 - 14)
                            timePos = fitz.Point(textPos1.x - strPart1_width,textPos1.y)
                            textPos2 = fitz.Point(timePos.x - strTime_width,textPos1.y)
                            # 計算頂部提示內容調整角度    
                            adjustTextRotation = 180
                                

                            # 浮水印起點
                            watermark_x1 = (ori_width-watermark_width)/2
                            watermark_y1 = (ori_height-watermark_height)/2
                            # 浮水印結束點
                            watermark_x2 = watermark_x1 + watermark_width
                            watermark_y2 = watermark_y1 + watermark_height
                            # 計算浮水印調整角度    
                            adjustRotation = 180

                        if (currentRotation==270):
                            # 頂部提示起點
                            rect_border_x1 = ori_width - rect_top - rect_height - rect_border_margin*2
                            rect_border_y1 = (rotated_width - total_str_width)/2
                            # 頂部提示結束點
                            rect_border_x2 = ori_width - rect_top
                            rect_border_y2 = (rotated_width - total_str_width)/2 + total_str_width + rect_border_margin * 2
                            # 頂部提示框文字與時間位置
                            textPos1 = fitz.Point(rect_border_x1 + rect_border_margin*2 + rect_height -14 , rect_border_y1 + rect_border_margin)
                            timePos = fitz.Point(textPos1.x, textPos1.y + strPart1_width)
                            textPos2 = fitz.Point(textPos1.x,timePos.y + strTime_width)
                            # 計算頂部提示內容調整角度    
                            adjustTextRotation = -90

                            # 浮水印起點
                            watermark_x1 = (ori_width-watermark_height)/2
                            watermark_y1 = (ori_height-watermark_width)/2
                            # 浮水印結束點
                            watermark_x2 = watermark_x1 + watermark_height
                            watermark_y2 = watermark_y1 + watermark_width
                            # 計算浮水印調整角度    
                            adjustRotation = -90
                        
                        # 產生頂部提示外框區域
                        rect_border_p1 = fitz.Point(rect_border_x1,rect_border_y1)
                        rect_border_p2 = fitz.Point(rect_border_x2,rect_border_y2)
                        rect_border = fitz.Rect(rect_border_p1.x,rect_border_p1.y,rect_border_p2.x,rect_border_p2.y)

                        # 產生浮水印區域
                        watermark_p1 = fitz.Point(watermark_x1,watermark_y1)
                        watermark_p2 = fitz.Point(watermark_x2,watermark_y2)
                        rect_watermark = fitz.Rect(watermark_p1.x,watermark_p1.y,watermark_p2.x,watermark_p2.y)

                        # 於 PDF 繪製上述各區域計算結果
                        # 繪製頂部提示區域
                        if(isNeedAnnot):
                            # 添加字段外框
                            annot_border = page.draw_rect(rect_border,color=black,fill=None,width=0.5,dashes=None)
                            # 添加字段
                            if(strPart1):
                                annot_text1 = page.insert_text(textPos1, strPart1,fontsize=8,fontname="china-t",color=black,rotate=adjustTextRotation)
                            if(isContainDate):
                                annot_time = page.insert_text(timePos, strTime,fontsize=8,fontname="cour",color=black,rotate=adjustTextRotation)
                            if(strPart2):
                                annot_text2 = page.insert_text(textPos2, strPart2,fontsize=8,fontname="china-t",color=black,rotate=adjustTextRotation)
                            
                        # 繪製圖片浮水印
                        if(isNeedWatermark):
                            # 讀取浮水印圖片檔
                            watermark_pic = open(watermark_pic_path, "rb").read()
                            # 添加浮水印
                            page.insert_image(rect_watermark, stream = watermark_pic ,rotate=adjustTextRotation)

                    # 儲存 PDF 檔案
                    pdfDoc.save(pdf_result)
                    pdfDoc.close()

                    # 顯示成功與否
                    resultData.at[index_file, "Status"] = "Success"
                    resultData.at[index_file, "Message"] = "-"
                    resultData.at[index_file, "Output Path"] = pdf_result
            else:
                raise Exception("該檔案不存在，或路徑輸入錯誤，請確認後再重新執行 ! " + pdf_list[index_file])
        # 擷取個別檔案進行浮水印轉換時發生的錯誤
        except Exception as e:
            # 顯示成功與否
            resultData.at[index_file, "Status"] = "Failure"
            resultData.at[index_file, "Message"] = str(e)
            resultData.at[index_file, "Output Path"] = "-"
            if(pdf_result and os.path.exists(pdf_result)):
                os.remove(pdf_result)

# 擷取系統錯誤，若錯誤則所有檔案都顯示失敗
except Exception as e:
    # 顯示成功與否
    resultData["Status"] = "Failure"
    resultData["Message"] = "Alteryx 解析 PDF 過程發生錯誤，請與 AI&T 同仁聯繫("+str(e)+")"
    resultData["Output Path"] = "-"
    if(pdf_result and os.path.exists(pdf_result)):
        os.remove(pdf_result)
Alteryx.write(resultData,1)
# Copyright © 2001-2022 Python Software Foundation; All Rights Reserved.
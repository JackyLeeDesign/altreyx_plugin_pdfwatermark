# List all non-standard packages to be imported by your 
# script here (only missing packages will be installed)
from ayx import Package
try:
    Package.installPackages(package=['pandas','pymupdf'], install_type="install --user")
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
                        # 獲取原頁面高度與寬度
                        page.set_rotation(0)
                        # 寬度
                        ori_total_width = page.rect.x1
                        # 高度
                        ori_total_height = page.rect.y1
                        page.set_rotation(currentRotation)

                        total_width  = ori_total_width
                        total_height = ori_total_height

                        # 提示字段Part1寬度
                        strPart1_width = len(strPart1)*8
                        # 提示字段Part2寬度
                        strPart2_width = len(strPart2)*8
                        # 時間字段寬度
                        strTime_width = len(strTime)*5
                        # 提示字段總寬度
                        total_str_width = strPart1_width + strPart2_width + strTime_width

                        # 字段之間的間距
                        rect_margin = 5
                        # 框線與字的間距
                        rect_border_margin = 8
                        # 文字框高度
                        rect_height = 8
                        # 文字框距離文件上方高度
                        rect_top = 20
                        
                        # 計算浮水印調整角度與各點座標調整變量
                        adjustRotation = 0
                        # if currentRotation == 90:
                        #     total_width = ori_total_height
                        #     total_height = ori_total_width
                        #     adjustRotation = currentRotation
                        
                        # 最大可填字數計算
                        # print((total_width-strTime_width-rect_border_margin*2-rect_margin*4)/8)

                        # 計算part1文字框的 P1(x,y), P2(x,y)座標
                        rect1_x1 = (total_width-total_str_width)/2
                        rect1_y1 = rect_top
                        rect1_x2 = rect1_x1 + strPart1_width + rect_margin
                        rect1_y2 = rect_top + rect_height
                        rect1_p1 = fitz.Point(rect1_x1,rect1_y1) #* page.derotation_matrix
                        rect1_p2 = fitz.Point(rect1_x2,rect1_y2) #* page.derotation_matrix
                        rect1 = fitz.Rect(rect1_p1.x,rect1_p1.y,rect1_p2.x,rect1_p2.y)

                        # 計算time文字框的 P1(x,y), P2(x,y)座標
                        rect_time_x1 = rect1_x2
                        rect_time_y1 = rect_top
                        rect_time_x2 = rect_time_x1 + strTime_width + rect_margin
                        rect_time_y2 = rect_top + rect_height
                        rect_time_p1 = fitz.Point(rect_time_x1,rect_time_y1) #* page.derotation_matrix
                        rect_time_p2 = fitz.Point(rect_time_x2,rect_time_y2) #* page.derotation_matrix
                        rect_time = fitz.Rect(rect_time_p1.x,rect_time_p1.y,rect_time_p2.x,rect_time_p2.y)

                        # 計算part2文字框的 P1(x,y), P2(x,y)座標
                        rect2_x1 = rect_time_x2
                        rect2_y1 = rect_top
                        rect2_x2 = rect2_x1 + strPart2_width + rect_margin
                        rect2_y2 = rect_top + rect_height
                        rect2_p1 = fitz.Point(rect2_x1,rect2_y1) #* page.derotation_matrix
                        rect2_p2 = fitz.Point(rect2_x2,rect2_y2) #* page.derotation_matrix
                        rect2 = fitz.Rect(rect2_p1.x,rect2_p1.y,rect2_p2.x,rect2_p2.y)

                        # 外框
                        rect_border_x1 = rect1_x1 - rect_border_margin
                        rect_border_y1 = rect_top - rect_border_margin
                        rect_border_x2 = rect2_x2 - rect_margin + rect_border_margin
                        rect_border_y2 = rect_top + rect_height + rect_border_margin
                        rect_border_p1 = fitz.Point(rect_border_x1,rect_border_y1) #* page.derotation_matrix
                        rect_border_p2 = fitz.Point(rect_border_x2,rect_border_y2) #* page.derotation_matrix
                        rect_border = fitz.Rect(rect_border_p1.x,rect_border_p1.y,rect_border_p2.x,rect_border_p2.y)

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
                        watermark_x1 = (total_width-watermark_width)/2
                        watermark_y1 = (total_height-watermark_height)/2
                        watermark_x2 = watermark_x1 + watermark_width
                        watermark_y2 = watermark_y1 + watermark_height
                        watermark_p1 = fitz.Point(watermark_x1,watermark_y1) #* page.derotation_matrix
                        watermark_p2 = fitz.Point(watermark_x2,watermark_y2) #* page.derotation_matrix
                        rect_watermark = fitz.Rect(watermark_p1.x,watermark_p1.y,watermark_p2.x,watermark_p2.y)
                        watermark_pic = open(watermark_pic_path, "rb").read()
                        # shape = page.new_shape()
                        # # draw the insertion points as red, filled dots
                        # shape.draw_rect(rect1)
                        # shape.draw_rect(rect2)
                        # shape.draw_rect(rect_time)
                        # shape.draw_rect(rect_border)
                        # shape.finish(width=0.3, color=(1,0,0), fill=(1,0,0))
                        # # store our work to the page
                        # shape.commit()

                        # 添加外框
                        if(isNeedAnnot):
                            annot_border = page.add_rect_annot(rect_border)
                            annot_border.set_border(width=0.5)
                            annot_border.set_colors(stroke=black)
                            annot_border.set_rotation(adjustRotation)
                            annot_border.update()
                            if(strPart1):
                                # 添加第一部分字段(日期前字段)
                                annot_part1 = page.add_freetext_annot(rect1, strPart1,fontsize=8,fontname="china-t",text_color=black,align=fitz.TEXT_ALIGN_CENTER)
                            if(isContainDate):
                                # 添加日期字段
                                annot_time = page.add_freetext_annot(rect_time, strTime,fontsize=8,fontname="cour",text_color=black,align=fitz.TEXT_ALIGN_CENTER)
                            if(strPart2):
                                # 添加第二部分字段(日期後字段)
                                annot_part2 = page.add_freetext_annot(rect2, strPart2,fontsize=8,fontname="china-t",text_color=black,align=fitz.TEXT_ALIGN_CENTER)
                        if(isNeedWatermark):
                            # 添加圖片浮水印
                            page.insert_image(rect_watermark, stream = watermark_pic)
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
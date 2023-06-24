import arcpy
def compare_fields(feature_class, field_name_fc, field_name_at, result_field):
    # قم بفتح الحقول للقراءة والكتابة
    fields = [field_name_fc, field_name_at, result_field, "property_classification"]
    # قم بالوصول إلى البيانات في feature class باستخدام كائن Cursor
    with arcpy.da.UpdateCursor(feature_class, fields) as cursor:
        for row in cursor:
            field_value_fc = row[0]
            field_value_at = row[1]
            property_classification = row[3]

            # قارن field_value_fc مع extracted_value إذا كانت field_value_at غير فارغة
            if field_value_at:
                start_index = len("https://ebranch.nwc.com.sa/Arabic/Pages/Customer.aspx?QRID=")
                extracted_value = field_value_at[start_index:]
                extracted_value = extracted_value.rstrip("'")  # إزالة العلامة ' من النهاية إذا كانت موجودة
                if field_value_fc == extracted_value:
                    row[2] = "TRUE"
                else:
                    row[2] = "FALSE"
            else:
                if not field_value_fc or property_classification in ["أرض فضاء", "تحت الإنشاء"]:
                    row[2] = "TRUE"
                else:
                    row[2] = "CHECK PHOTO"
            cursor.updateRow(row)
# تحديد المعلم (feature class) واسم الحقل في feature class وattribute table واسم الحقل للنتيجة
feature_class = r"D:/test/Matching.gdb/AGP_METERINGPOINT_All_Check/AGP_METERINGPOINT_GIS"
field_name_fc = "nwc_barcode_plate"
field_name_at = "Plate_QR"  # اسم الحقل في attribute table
result_field = "Comparison_Result_PALTE"  # اسم الحقل للنتيجة
# الفيلد الخاص لتشيك العدادات
def compare_Water_N(feature_class1, field_name_fc1, field_name_at1, result_field1, property_classification1, custom_service1, DistanceW_Customer2):
    # قم بفتح الحقول للقراءة والكتابة
    fields1 = [field_name_fc1, field_name_at1, result_field1, property_classification1, custom_service1, DistanceW_Customer2]

    # قم بالوصول إلى البيانات في feature class باستخدام كائن Cursor
    with arcpy.da.UpdateCursor(feature_class1, fields1) as cursor:
        for row in cursor:
            field_value_fc1 = row[0]
            field_value_at1 = row[1]
            property_classification1 = row[3]
            custom_service1 = row[4]
            DistanceW_Customer2 = row[5]
            if field_value_fc1 == field_value_at1 and custom_service1 in ["FullMatch", "PartMatch"]:
                row[2] = "TRUE"
            elif custom_service1 == "FullMatch" and DistanceW_Customer2 <= 100 or custom_service1 == "PartMatch" and DistanceW_Customer2 <= 100:
                row[2] = "TRUE"
            elif custom_service1 == "FullMatch" and DistanceW_Customer2 >= 100 or custom_service1 == "PartMatch" and DistanceW_Customer2 >= 100:
                row[2] = "Check Photo"
            elif field_value_fc1 == field_value_at1 and property_classification1 == "أرض فضاء":
                if not field_value_fc1 or field_value_fc1 == "":
                    row[2] = "NOserial"
                else:
                    row[2] = "Not Linked"
            elif field_value_fc1 == field_value_at1 and custom_service1 == "Part Match":
                row[2] = "TRUE"
            elif not field_value_fc1 or field_value_fc1 == "":
                row[2] = "NO Serial"
            elif field_value_fc1 == field_value_at1:
                row[2] = "Not Linked"
            elif field_value_fc1 != field_value_at1 and field_name_fc1 == "water_meter_no" and (
                    (field_value_fc1 and field_value_at1) or (not field_value_fc1 and field_value_at1)):
                row[2] = "FALSE"
            else:
                row[2] = "CHECK PHOTO"
            cursor.updateRow(row)
# تحديد المعلم (feature class) واسم الحقل في feature class وattribute table واسم الحقل للنتيجة
feature_class1 = r"D:/test/Matching.gdb/AGP_METERINGPOINT_All_Check/AGP_METERINGPOINT_GIS"
field_name_fc1 = "water_meter_no"
field_name_at1 = "Meter_QR"  # اسم الحقل في attribute table
result_field1 = "test_meter"  # اسم الحقل للنتيجة
property_classification1 = "property_classification"
custom_service1 = "JoinCheckW_Customer2"
DistanceW_Customer2 = "DistanceW_Customer2"

def NOTE (feature_class1, coordinate_place_DATA, water_meter_no, result_field2):
    # قم بفتح الحقول للقراءة والكتابة
    fields1 = [coordinate_place_DATA, water_meter_no, result_field2 ]

    # قم بالوصول إلى البيانات في feature class باستخدام كائن Cursor
    with arcpy.da.UpdateCursor(feature_class1, fields1) as cursor:
        for row in cursor:
            coordinate_place_DATA = row[0]
            water_meter_no = row[1]
            if coordinate_place_DATA == "العداد" and (not water_meter_no or water_meter_no == ""):
                    row[2] = "FALSE"
            elif coordinate_place_DATA == "منتصف المبني" and water_meter_no:
                        row[2] = " تغيره من مننتصف المبنى الى عداد"
            else:
                row[2] = " "
            cursor.updateRow(row)

# تحديد المعلم (feature class) واسم الحقل في feature class وattribute table واسم الحقل للنتيجة
feature_class1 = r"D:/test/Matching.gdb/AGP_METERINGPOINT_All_Check/AGP_METERINGPOINT_GIS"
coordinate_place_DATA = "coordinate_place"
water_meter_no = "water_meter_no"  # اسم الحقل في attribute table
result_field2 = "not_"
# اسم الحقل للنتيجة
# استدعاء الدالة للمقارنة وتحديث النتائج
compare_Water_N(feature_class1, field_name_fc1, field_name_at1, result_field1, property_classification1, custom_service1, DistanceW_Customer2)
compare_fields(feature_class, field_name_fc, field_name_at, result_field)
NOTE (feature_class1, coordinate_place_DATA, water_meter_no, result_field2)


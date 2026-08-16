
# Graduation Lineup Portal - Version 2

## الجديد
- رفع ملفات Excel بصيغة XLSX مباشرة.
- استخراج آخر 4 أرقام من رقم الهاتف تلقائياً.
- تخزين آخر 4 أرقام فقط في قاعدة البيانات.
- إظهار يوم البروفة ووقت البروفة والملاحظات للطالب.
- ما زال رفع CSV مدعوماً.

## أعمدة Excel المطلوبة
يمكن استخدام الأسماء الإنجليزية التالية:
student_id
student_name
major
phone_number
lineup_number
rehearsal_day
rehearsal_time
notes

أو العناوين العربية:
الرقم الجامعي
اسم الطالب
التخصص
رقم الهاتف
رقم الاصطفاف
يوم البروفة
وقت البروفة
ملاحظات

الأعمدة الإلزامية:
student_id / الرقم الجامعي
student_name / اسم الطالب
major / التخصص
phone_number / رقم الهاتف
lineup_number / رقم الاصطفاف

الأعمدة الاختيارية:
rehearsal_day / يوم البروفة
rehearsal_time / وقت البروفة
notes / ملاحظات

## تحديث GitHub
استبدل الملفات التالية في المستودع:
- app.py
- requirements.txt
- templates/index.html
- templates/admin_dashboard.html

ويمكن الإبقاء على:
- render.yaml
- templates/base.html
- templates/admin_login.html
- static/style.css

لكن رفع النسخة الكاملة المرفقة هو الأسهل.

بعد Commit، سيبدأ Render Deploy تلقائياً. إذا لم يبدأ:
Manual Deploy > Deploy latest commit

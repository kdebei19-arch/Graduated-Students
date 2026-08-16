
# بوابة أرقام الاصطفاف - نسخة جاهزة لـ Render

## 1) إنشاء كلمة مرور الإدارة
نفّذ محليًا:
pip install Werkzeug
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('ضع-كلمة-مرور-قوية-هنا'))"

انسخ الناتج كاملًا.

## 2) الرفع إلى GitHub
- أنشئ Repository جديدًا.
- ارفع جميع ملفات المشروع إليه.

## 3) النشر على Render
- اختر New > Blueprint.
- اربط مستودع GitHub.
- Render سيقرأ render.yaml.
- عند طلب ADMIN_PASSWORD_HASH ألصق قيمة الـ hash التي أنشأتها.
- اضغط Deploy.

بعد اكتمال النشر ستحصل على رابط عام ينتهي بـ onrender.com.

## 4) صفحة الإدارة
افتح:
https://YOUR-SITE.onrender.com/admin

## 5) ملف الطلبة
CSV بالأعمدة:
student_id,student_name,major,phone_last4,lineup_number,lineup_location,rehearsal_time,notes

المطلوب إلزاميًا:
student_id
student_name
major
phone_last4
lineup_number

## ملاحظة
Render يدعم Flask عبر Python وGunicorn. النسخة المجانية من PostgreSQL تنتهي بعد 30 يومًا، لذا هي مناسبة للتجربة أو لاستخدام مؤقت قريب من موعد الحفل.

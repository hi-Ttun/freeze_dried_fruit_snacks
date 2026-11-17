"""Tạo dữ liệu mẫu chuẩn TMĐT: danh mục, sản phẩm cao cấp, lô hàng FEFO, nhóm quyền.

Bộ dữ liệu thực tế dựa trên sản phẩm Sầu riêng sấy (tham khảo Vitamin House)
và nông sản sấy thăng hoa / hạt dinh dưỡng tiêu chuẩn Việt Nam.
"""
from datetime import timedelta

from django.contrib.auth.models import Group, Permission, User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from shop.models import Category, Lot, Product, Variant

CATALOG = [
    {
        "category": ("Trái cây sấy thăng hoa", "trai-cay-say-thang-hoa", 1),
        "products": [
            {
                "name": "Sầu riêng sấy thăng hoa Monthong thượng hạng",
                "slug": "sau-rieng-say-thang-hoa",
                "short": "Múi sầu riêng Monthong tươi tuyển chọn, sấy thăng hoa giòn xốp giữ trọn vị béo ngọt tự nhiên, không cholesterol.",
                "description": (
                    "Sản phẩm được chế biến từ những múi sầu riêng Monthong chín cây tự nhiên tại miệt vườn miền Tây. "
                    "Bằng công nghệ sấy thăng hoa (Freeze Drying) hiện đại ở nhiệt độ âm sâu -40°C trong môi trường chân không, "
                    "từng thớ thịt sầu riêng vẫn giữ nguyên cấu trúc giòn xốp, hương thơm nồng nàn đặc trưng và vị ngọt béo ngậy "
                    "mà không hề thêm đường, dầu chiên hay chất bảo quản. Thích hợp làm món ăn vặt lành mạnh, quà biếu cao cấp "
                    "hoặc bổ sung năng lượng tiện lợi mỗi ngày."
                ),
                "ingredients": "100% Cơm sầu riêng Monthong chín cây tự nhiên",
                "nutrition": "Trong 100g: Năng lượng 440 kcal, Đạm 5.2g, Chất béo 11.8g, Carbohydrate 76.5g, Chất xơ 4.8g, Canxi 35mg, Kali 610mg.",
                "origin": "Vùng trồng Chợ Lách (Bến Tre) / Cai Lậy (Tiền Giang)",
                "certificates": "VietGAP, HACCP, ISO 22000:2018",
                "featured": True,
                "variants": [("Túi 50g", 50, 89000), ("Túi zip 100g", 100, 169000), ("Túi đại 215g", 215, 329000)],
                "source_note": "HTX Nông nghiệp Bến Tre - Lô xuất khẩu VietGAP",
            },
            {
                "name": "Dâu tây Đà Lạt sấy thăng hoa nguyên trái",
                "slug": "dau-tay-da-lat-say-thang-hoa",
                "short": "Dâu tây tươi Đà Lạt nguyên quả giòn tan, vị chua ngọt tự nhiên, giàu Vitamin C và chất chống oxy hóa.",
                "description": (
                    "Những quả dâu tây tươi mọng nước được thu hái thủ công tại các nhà vườn công nghệ cao Đà Lạt vào buổi sớm. "
                    "Công nghệ sấy thăng hoa rút hết 98% độ ẩm nhưng giữ nguyên vẹn sắc đỏ tự nhiên, hình dáng quả và hàm lượng "
                    "Vitamin C quý giá. Khi ăn bạn sẽ cảm nhận được độ giòn xốp tan ngay trong miệng, vị chua ngọt thanh mát cực kỳ kích thích vị giác."
                ),
                "ingredients": "100% Dâu tây tươi Đà Lạt tuyển chọn",
                "nutrition": "Trong 100g: Năng lượng 335 kcal, Protein 4.8g, Chất béo 0.8g, Carbohydrate 72.0g, Chất xơ 7.2g, Vitamin C 280mg.",
                "origin": "Trại Mát, Phường 11, TP. Đà Lạt, Lâm Đồng",
                "certificates": "VietGAP, OCOP 4 sao tỉnh Lâm Đồng",
                "featured": True,
                "variants": [("Túi 30g", 30, 49000), ("Túi 60g", 60, 95000), ("Hũ nắp nhôm 100g", 100, 149000)],
                "source_note": "Nông trại Dâu tây Công nghệ cao Trại Mát, Đà Lạt",
            },
            {
                "name": "Xoài cát Chu sấy thăng hoa giòn nhẹ",
                "slug": "xoai-say-thang-hoa",
                "short": "Xoài cát Chu chín vàng ngọt thơm, giòn nhẹ xốp mịn, giàu Vitamin A, ăn liền hoặc mix sữa chua.",
                "description": (
                    "Được làm từ những trái xoài cát Chu nức tiếng của Đồng Tháp khi vừa chín tới đạt độ ngọt lý tưởng. "
                    "Từng lát xoài vàng ươm được cắt vừa ăn và sấy thăng hoa, tạo nên miếng xoài khô giòn nhẹ mà tan dần nơi đầu lưỡi "
                    "với hương thơm nhiệt đới đặc trưng."
                ),
                "ingredients": "100% Xoài cát Chu chín tự nhiên",
                "nutrition": "Trong 100g: Năng lượng 360 kcal, Protein 3.1g, Chất béo 0.6g, Carbohydrate 82.0g, Chất xơ 5.0g, Vitamin A 1200 IU.",
                "origin": "Cao Lãnh, Đồng Tháp",
                "certificates": "GlobalGAP, HACCP",
                "featured": True,
                "variants": [("Túi 30g", 30, 45000), ("Túi zip 80g", 80, 115000)],
                "source_note": "Vùng trồng Xoài Cao Lãnh đạt chuẩn GlobalGAP",
            },
            {
                "name": "Mít chín cây sấy thăng hoa giòn xốp",
                "slug": "mit-say-thang-hoa",
                "short": "Mít Thái chín cây sấy giòn xốp, giữ trọn sắc vàng ươm và hương thơm lừng tự nhiên.",
                "description": (
                    "Khác biệt hoàn toàn với mít chiên dầu thông thường, mít sấy thăng hoa giữ được trọn vẹn vị ngọt thanh mát, "
                    "không hề gắt dầu hay dính tay. Múi mít xốp phồng, giòn rụm và đậm vị ngọt lành của đất trời phương Nam."
                ),
                "ingredients": "100% Mít Thái ruột đỏ chín cây",
                "nutrition": "Trong 100g: Năng lượng 380 kcal, Protein 3.8g, Chất béo 1.2g, Carbohydrate 85.0g, Chất xơ 6.5g, Kali 540mg.",
                "origin": "Bình Phước, Việt Nam",
                "certificates": "VietGAP, ISO 22000",
                "featured": False,
                "variants": [("Túi 50g", 50, 59000), ("Túi zip 100g", 100, 109000)],
                "source_note": "Hợp tác xã Nông nghiệp Chơn Thành, Bình Phước",
            },
            {
                "name": "Chuối Laba sấy thăng hoa ngọt thanh",
                "slug": "chuoi-say-thang-hoa",
                "short": "Chuối Laba đặc sản sấy thăng hoa giòn rụm, ngọt dịu tự nhiên, bổ sung kali và năng lượng nhanh.",
                "description": (
                    "Chuối Laba - giống chuối tiến vua nức tiếng vùng cao nguyên Lâm Viên với độ dẻo và hương thơm sâu. "
                    "Sau quy trình sấy thăng hoa khép kín, từng lát chuối trở nên giòn tan, ngọt bùi dịu nhẹ, là món ăn vặt lý tưởng "
                    "cho trẻ nhỏ và người tập luyện thể thao."
                ),
                "ingredients": "100% Chuối Laba chín tự nhiên",
                "nutrition": "Trong 100g: Năng lượng 350 kcal, Protein 4.0g, Carbohydrate 78.0g, Chất xơ 5.8g, Kali 850mg.",
                "origin": "Đơn Dương, Lâm Đồng",
                "certificates": "VietGAP, OCOP 3 sao",
                "featured": False,
                "variants": [("Túi 40g", 40, 39000), ("Túi zip 90g", 90, 79000)],
                "source_note": "Nông trại Chuối Laba Đơn Dương, Lâm Đồng",
            },
            {
                "name": "Thanh long ruột đỏ sấy giòn giàu Antioxidant",
                "slug": "thanh-long-ruot-do-say-thang-hoa",
                "short": "Sắc đỏ tím tự nhiên giàu Anthocyanin, vị chua ngọt thanh mát, hỗ trợ làm đẹp da và tiêu hóa.",
                "description": (
                    "Thanh long ruột đỏ tươi được sấy thăng hoa giúp bảo toàn tối đa hoạt chất chống oxy hóa tự nhiên Anthocyanin "
                    "và chất xơ hòa tan. Từng miếng thanh long giòn xốp với hạt li ti vui miệng mang đến trải nghiệm thưởng thức mới lạ."
                ),
                "ingredients": "100% Thanh long ruột đỏ Tiền Giang",
                "nutrition": "Trong 100g: Năng lượng 320 kcal, Protein 3.5g, Carbohydrate 68.0g, Chất xơ 8.5g, Vitamin C 65mg.",
                "origin": "Chợ Gạo, Tiền Giang",
                "certificates": "VietGAP, HACCP",
                "featured": False,
                "variants": [("Túi 35g", 35, 49000), ("Túi zip 80g", 80, 99000)],
                "source_note": "Vùng trồng Thanh long Chợ Gạo, Tiền Giang",
            },
        ],
    },
    {
        "category": ("Hạt dinh dưỡng", "hat-dinh-duong", 2),
        "products": [
            {
                "name": "Hạt Macca nứt vỏ Đắk Lắk (kèm dụng cụ tách)",
                "slug": "hat-macca-nut-vo",
                "short": "Macca nứt vỏ tự nhiên hạt to đều, vị béo ngậy bùi thơm chuẩn xuất khẩu, tặng kèm dụng cụ khui.",
                "description": (
                    "Hạt macca Đắk Lắk được mệnh danh là 'nữ hoàng các loại hạt' nhờ hàm lượng chất béo không bão hòa đơn và Omega-7 dồi dào. "
                    "Hạt được sấy chín ở nhiệt độ thấp để giữ tối đa dưỡng chất, vỏ nứt sẵn tinh tế giúp bạn dễ dàng tách ăn bằng dụng cụ khui kèm theo."
                ),
                "ingredients": "100% Hạt mắc ca nứt vỏ sấy chín",
                "nutrition": "Trong 100g: Năng lượng 718 kcal, Đạm 7.9g, Chất béo 75.8g (chủ yếu Omega-7 và Omega-9), Chất xơ 8.6g.",
                "origin": "Krông Năng, Đắk Lắk",
                "certificates": "OCOP 4 sao, VietGAP",
                "featured": True,
                "variants": [("Hũ 250g", 250, 125000), ("Hũ 500g", 500, 239000)],
                "source_note": "HTX Nông nghiệp Macca Krông Năng, Đắk Lắk",
            },
            {
                "name": "Hạt điều rang củi Bình Phước A cồ",
                "slug": "hat-dieu-rang-cui",
                "short": "Hạt điều loại A cồ thượng hạng rang củi giữ vỏ lụa, vị giòn rụm béo bùi đậm đà.",
                "description": (
                    "Tuyển chọn từ những hạt điều Bình Phước loại A cồ to tròn đều hạt nhất. "
                    "Rang củi truyền thống với lượng muối biển cực nhỏ giúp hạt giữ trọn vị ngọt tự nhiên, "
                    "lớp vỏ lụa bảo vệ hạt luôn giòn thơm mà không bị nhiễm mặn."
                ),
                "ingredients": "99.5% Hạt điều vỏ lụa loại A, 0.5% muối biển",
                "nutrition": "Trong 100g: Năng lượng 553 kcal, Đạm 18.2g, Chất béo 43.8g, Magie 292mg, Sắt 6.7mg.",
                "origin": "Bù Đăng, Bình Phước",
                "certificates": "Chỉ dẫn địa lý Bình Phước, HACCP",
                "featured": True,
                "variants": [("Hũ 250g", 250, 99000), ("Hộp 500g", 500, 189000)],
                "source_note": "Cơ sở Chế biến Hạt điều Bù Đăng, Bình Phước",
            },
            {
                "name": "Hạnh nhân rang bơ mộc vỏ mỏng",
                "slug": "hanh-nhan-rang-bo",
                "short": "Hạnh nhân nguyên vỏ mỏng rang bơ thơm lừng, giòn rụm, giàu Vitamin E và canxi.",
                "description": (
                    "Hạnh nhân nhập khẩu với lớp vỏ mỏng dễ tách, được rang cùng bơ tự nhiên tạo nên hương vị bùi béo khó cưỡng. "
                    "Giàu chất chống oxy hóa, tốt cho tim mạch và làn da."
                ),
                "ingredients": "99% Hạnh nhân nguyên vỏ, 1% bơ tự nhiên",
                "nutrition": "Trong 100g: Năng lượng 579 kcal, Protein 21.1g, Chất béo 49.9g, Chất xơ 12.5g, Vitamin E 25.6mg.",
                "origin": "Nhập khẩu chuẩn California, Mỹ",
                "certificates": "USDA Organic, FDA",
                "featured": False,
                "variants": [("Hũ 250g", 250, 119000), ("Hũ 500g", 500, 229000)],
                "source_note": "Lô hàng nhập khẩu chính ngạch California, USA",
            },
            {
                "name": "Hạt dẻ cười Mỹ sấy mộc không tẩy trắng",
                "slug": "hat-de-cuoi-my",
                "short": "Hạt dẻ cười mở miệng tự nhiên, không tẩy trắng hóa chất, vị ngọt bùi tự nhiên giàu lutein.",
                "description": (
                    "Hạt dẻ cười nhập khẩu trực tiếp từ Mỹ, đảm bảo 100% vỏ màu ngà tự nhiên không qua tẩy trắng. "
                    "Hạt xanh ngọc bích, béo bùi, giàu chất xơ và chất chống oxy hóa lutein bảo vệ mắt."
                ),
                "ingredients": "100% Hạt dẻ cười sấy mộc",
                "nutrition": "Trong 100g: Năng lượng 562 kcal, Đạm 20.3g, Chất béo 45.3g, Kali 1025mg, Lutein dồi dào.",
                "origin": "California, Mỹ",
                "certificates": "FDA, Non-GMO Project Verified",
                "featured": False,
                "variants": [("Hũ 200g", 200, 135000), ("Hũ 450g", 450, 289000)],
                "source_note": "Lô nhập khẩu chính ngạch từ Wonderful Pistachios, USA",
            },
        ],
    },
    {
        "category": ("Hạt & Quả sấy hỗn hợp", "trail-mix-granola", 3),
        "products": [
            {
                "name": "Daily Trail Mix - Hạt dinh dưỡng & Quả sấy",
                "slug": "daily-trail-mix",
                "short": "Sự kết hợp hoàn hảo giữa Macca, Hạt điều, Hạnh nhân và Dâu tây, Xoài sấy thăng hoa.",
                "description": (
                    "Công thức tỷ lệ vàng giữa các loại hạt béo bùi và trái cây sấy chua ngọt tự nhiên. "
                    "Cung cấp nguồn năng lượng sạch, chất xơ và vitamin dồi dào cho bữa phụ văn phòng hoặc người ăn kiêng."
                ),
                "ingredients": "Hạt điều (25%), Macca (20%), Hạnh nhân (20%), Dâu tây sấy (15%), Xoài sấy (20%)",
                "nutrition": "Trong 100g: Năng lượng 495 kcal, Đạm 14.5g, Chất béo tốt 31.0g, Carbohydrate 48.0g, Chất xơ 7.8g.",
                "origin": "Việt Nam",
                "certificates": "HACCP, ISO 22000",
                "featured": True,
                "variants": [("Hộp 7 gói chia nhỏ (175g)", 175, 119000), ("Hũ lớn 350g", 350, 199000)],
                "source_note": "Xưởng chế biến và đóng gói NutriSnack Certified ISO 22000",
            },
            {
                "name": "Granola siêu hạt nướng mật ong hoa nhãn",
                "slug": "granola-sieu-hat",
                "short": "Granola giòn rụm với 85% hạt dinh dưỡng nướng mật ong hoa nhãn nguyên chất, không đường tinh luyện.",
                "description": (
                    "Granola cao cấp với tỷ lệ hạt dinh dưỡng lên đến 85% kết hợp cùng yến mạch nguyên cám Úc. "
                    "Nướng chậm cùng mật ong hoa nhãn tự nhiên mang đến vị giòn rụm, ngọt thanh dễ chịu. "
                    "Hoàn hảo khi dùng kèm sữa tươi không đường hoặc sữa chua Hy Lạp."
                ),
                "ingredients": "Yến mạch Úc (15%), Macca (20%), Hạt điều (20%), Hạnh nhân (20%), Hạt bí xanh (15%), Mật ong hoa nhãn (10%)",
                "nutrition": "Trong 100g: Năng lượng 460 kcal, Đạm 16.0g, Chất béo tốt 28.0g, Beta-Glucan 3.5g, Carbs 42.0g.",
                "origin": "Việt Nam",
                "certificates": "VietGAP, HACCP",
                "featured": False,
                "variants": [("Hũ 250g", 250, 95000), ("Túi zip 500g", 500, 179000)],
                "source_note": "Xưởng chế biến và đóng gói NutriSnack Certified ISO 22000",
            },
        ],
    },
    {
        "category": ("Hộp quà & Combo dinh dưỡng", "combo-qua-tang", 4),
        "products": [
            {
                "name": "Hộp quà Nông Sản Lành - Golden Harvest",
                "slug": "hop-qua-nong-san-lanh",
                "short": "Set quà sang trọng kết hợp Sầu riêng Monthong, Dâu tây sấy và Macca nứt vỏ kèm thiệp chúc.",
                "description": (
                    "Hộp quà tri ân sang trọng với thiết kế hộp cứng dập kim cao cấp. "
                    "Bên trong gồm 3 hũ nông sản sấy tuyển chọn: Sầu riêng Monthong (100g), Dâu tây Đà Lạt sấy (100g) "
                    "và Hạt Macca Đắk Lắk (250g). Món quà sức khỏe tinh tế và ý nghĩa dành tặng đối tác, khách hàng và người thân."
                ),
                "ingredients": "Sầu riêng sấy (100g), Dâu tây sấy (100g), Hạt macca (250g)",
                "nutrition": "Sản phẩm tổng hợp các dưỡng chất tự nhiên từ trái cây sấy và hạt dinh dưỡng cao cấp.",
                "origin": "Việt Nam",
                "certificates": "Đóng gói theo tiêu chuẩn ISO 22000",
                "featured": True,
                "variants": [("Hộp quà cao cấp 450g", 450, 429000)],
                "source_note": "Bộ quà tặng giới hạn NutriSnack Seasonal Gift",
            },
            {
                "name": "Combo Văn Phòng Ăn Vặt Lành Mạnh (7 Ngày)",
                "slug": "combo-van-phong-7-ngay",
                "short": "7 gói snack sấy giòn tiện lợi chia đều cho 7 ngày làm việc tràn đầy năng lượng và tỉnh táo.",
                "description": (
                    "Giải pháp ăn vặt healthy hoàn hảo cho dân công sở. Mỗi ngày một gói snack định lượng chuẩn 30g - 35g "
                    "giúp bổ sung năng lượng nhanh, chống đói giữa giờ làm việc mà không lo tăng cân hay tích mỡ xấu."
                ),
                "ingredients": "Gồm 7 gói riêng biệt: 2 gói Sầu riêng sấy, 2 gói Dâu tây sấy, 1 gói Xoài sấy, 2 gói Trail Mix hạt",
                "nutrition": "Mỗi khẩu phần cung cấp khoảng 120-150 kcal năng lượng lành mạnh.",
                "origin": "Việt Nam",
                "certificates": "HACCP, ISO 22000",
                "featured": False,
                "variants": [("Hộp 7 gói tuần", 225, 249000)],
                "source_note": "Bộ quà tặng tiện ích NutriSnack Office Pack",
            },
        ],
    },
]

SALES_PERMS = [
    "view_order", "change_order", "view_orderitem", "view_payment", "change_payment",
    "view_shipment", "add_shipment", "change_shipment", "view_statushistory",
    "view_product", "view_variant", "view_lot",
]
WAREHOUSE_PERMS = [
    "view_product", "view_variant", "view_lot", "add_lot", "change_lot",
    "view_order", "change_order", "view_orderitem", "view_shipment", "add_shipment", "change_shipment",
]


class Command(BaseCommand):
    help = "Tạo dữ liệu mẫu chuẩn TMĐT: 14 sản phẩm, danh mục, lô hàng FEFO và nhóm quyền."

    def add_arguments(self, parser):
        parser.add_argument("--admin-password", help="Tạo/cập nhật tài khoản superuser 'admin' với mật khẩu này")
        parser.add_argument("--demo-password", help="Tạo tài khoản nhân viên sales_demo, warehouse_demo với mật khẩu này")

    @transaction.atomic
    def handle(self, *args, **opts):
        today = timezone.localdate()
        lot_codes = []
        index = 0
        for block in CATALOG:
            name, slug, order = block["category"]
            category, _ = Category.objects.update_or_create(slug=slug, defaults={"name": name, "order": order})
            for pinfo in block["products"]:
                index += 1
                product, _ = Product.objects.update_or_create(
                    slug=pinfo["slug"],
                    defaults={
                        "category": category,
                        "name": pinfo["name"],
                        "short_description": pinfo["short"],
                        "description": pinfo["description"],
                        "ingredients": pinfo["ingredients"],
                        "nutrition": pinfo["nutrition"],
                        "origin": pinfo["origin"],
                        "certificates": pinfo["certificates"],
                        "is_featured": pinfo["featured"],
                        "is_active": True,
                    },
                )
                for label, grams, price in pinfo["variants"]:
                    sku = f"NS{index:02d}-{grams}G"
                    variant, _ = Variant.objects.update_or_create(
                        sku=sku, defaults={"product": product, "label": label, "weight_g": grams, "price": price, "is_active": True}
                    )
                    specs = [(f"{sku}-L1", 120, 50), (f"{sku}-L2", 300, 80)]
                    if index == 1 and grams == 50:  # dữ liệu demo FEFO và cảnh báo hạn dùng cho sản phẩm lõi
                        specs += [(f"{sku}-L0", 15, 10), (f"{sku}-LX", -5, 5)]
                    for code, days, qty in specs:
                        lot, _ = Lot.objects.update_or_create(
                            code=code,
                            defaults={
                                "variant": variant,
                                "produced_on": today - timedelta(days=30),
                                "expires_on": today + timedelta(days=days),
                                "quantity_in": qty,
                                "quantity_left": qty,
                                "source_note": pinfo.get("source_note", "Nông trại đạt chuẩn VietGAP"),
                            },
                        )
                        lot_codes.append((code, days))

        self._groups()
        self._users(opts.get("admin_password"), opts.get("demo_password"))
        self.stdout.write(self.style.SUCCESS(f"Đã cập nhật thành công {index} sản phẩm chuẩn TMĐT vào hệ thống."))
        self.stdout.write("Một số mã lô hàng để thử tính năng tra cứu nguồn gốc (Traceability):")
        for code, days in lot_codes[:6]:
            self.stdout.write(f"  • {code} (Hạn dùng sau {days} ngày)")

    def _groups(self):
        for name, codenames in (("Sales", SALES_PERMS), ("Warehouse", WAREHOUSE_PERMS)):
            group, _ = Group.objects.get_or_create(name=name)
            group.permissions.set(Permission.objects.filter(codename__in=codenames))

    def _users(self, admin_password, demo_password):
        if admin_password:
            admin, _ = User.objects.get_or_create(username="admin", defaults={"email": "admin@example.com"})
            admin.is_staff = admin.is_superuser = True
            admin.set_password(admin_password)
            admin.save()
            self.stdout.write("Đã tạo/cập nhật tài khoản admin.")
        if demo_password:
            for username, group_name in (("sales_demo", "Sales"), ("warehouse_demo", "Warehouse")):
                user, _ = User.objects.get_or_create(username=username)
                user.is_staff = True
                user.set_password(demo_password)
                user.save()
                user.groups.set([Group.objects.get(name=group_name)])
            self.stdout.write("Đã tạo tài khoản sales_demo, warehouse_demo.")

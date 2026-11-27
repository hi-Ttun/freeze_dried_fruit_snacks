import logging
import re
import requests
from django.conf import settings
from .models import Category, Product

logger = logging.getLogger(__name__)

HANDOFF_KEYWORDS = [
    "gặp nhân viên", "tư vấn viên", "người thật", "chăm sóc khách hàng", "cskh",
    "hotline", "gọi điện", "zalo", "khiếu nại", "đổi trả", "hoàn tiền", "hàng hỏng",
    "hàng hư", "bể vỡ", "móp", "hư", "sỉ", "mua buôn", "bán buôn", "đại lý",
    "chiết khấu lớn", "hóa đơn vat", "hóa đơn đỏ", "doanh nghiệp", "quà tết công ty",
    "liên hệ trực tiếp", "nói chuyện với người", "gặp hỗ trợ", "gặp sale"
]


def check_handoff_trigger(message: str) -> bool:
    """Kiểm tra xem câu hỏi có thuộc các trường hợp cần chuyển tiếp người thật hay không."""
    msg = message.lower().strip()
    return any(kw in msg for kw in HANDOFF_KEYWORDS)


def get_handoff_response() -> dict:
    hotline = getattr(settings, "SITE_HOTLINE", "0901234567") or "0901234567"
    zalo = getattr(settings, "SITE_ZALO", f"https://zalo.me/{hotline}")
    email = getattr(settings, "SITE_CONTACT_EMAIL", "nutrisnack@gmail.com")

    return {
        "reply": (
            "Dạ, vấn đề này cần được **Chuyên viên tư vấn người thật** của NutriSnack hỗ trợ trực tiếp "
            "để giải quyết nhanh chóng và chu đáo nhất cho bạn ạ! 🌱\n\n"
            "Bạn có thể kết nối ngay với tư vấn viên qua Hotline, Zalo hoặc để lại số điện thoại bên dưới, "
            "nhân viên sẽ liên hệ lại ngay trong 5 - 10 phút nhé!"
        ),
        "is_handoff": True,
        "handoff_info": {
            "hotline": hotline,
            "zalo": zalo,
            "email": email,
        },
        "suggestions": [
            f"📞 Gọi Hotline: {hotline}",
            "💬 Chat Zalo tư vấn viên",
            "Xem chính sách đổi trả"
        ]
    }


def _build_system_context() -> str:
    """Tạo bản tóm tắt tri thức sản phẩm của NutriSnack cho AI."""
    products_info = []
    try:
        products = Product.objects.filter(is_active=True).prefetch_related("variants")
        for p in products[:15]:
            variants_str = ", ".join([f"{v.label}: {v.price:,}đ" for v in p.variants.all()])
            products_info.append(
                f"- {p.name}: {p.short_description}. Thành phần: {p.ingredients or 'Nguyên chất'}. "
                f"Xuất xứ: {p.origin or 'Việt Nam'}. Quy cách & giá: {variants_str}"
            )
    except Exception:
        products_info.append(
            "- Sầu riêng sấy thăng hoa Monthong/Ri6: 100% cơm sầu riêng, giòn xốp tan trong miệng, không đường, 50g: 89.000đ.\n"
            "- Dâu tây Đà Lạt sấy thăng hoa: Dâu tươi Đà Lạt nguyên quả, chua ngọt thanh mát, 50g: 65.000đ.\n"
            "- Xoài sấy thăng hoa Cát Chu: Vị ngọt tự nhiên, dẻo xốp, 50g: 48.000đ.\n"
            "- Mít sấy thăng hoa: Giòn rụm thơm lừng, 50g: 45.000đ.\n"
            "- Hạt Macca nứt vỏ Đắk Lắk: Kèm đồ khui, béo bùi, hũ 250g: 110.000đ, hũ 500g: 210.000đ.\n"
            "- Hạt điều rang củi Bình Phước: Rang thủ công giữ vỏ lụa, hũ 250g: 75.000đ, hũ 500g: 145.000đ.\n"
            "- Granola siêu hạt nướng mật ong: Yến mạch & 7 loại hạt, hũ 500g: 135.000đ."
        )

    return (
        "Bạn là NutriBot - Trợ lý ảo AI thông minh, thân thiện của thương hiệu nông sản sạch NutriSnack.\n"
        "Văn phong: Lịch sự, lễ phép (dạ, vâng), dùng icon trái cây thân thiện, tư vấn ngắn gọn, dễ hiểu.\n"
        "THÔNG TIN DOANH NGHIỆP & CHÍNH SÁCH:\n"
        "- Công nghệ cốt lõi: Sấy thăng hoa (Freeze-drying) ở nhiệt độ âm sâu -40°C trong môi trường chân không, "
        "giữ nguyên 95% vitamin, khoáng chất, màu sắc và hương vị tự nhiên, giòn xốp tan trong miệng, KHÔNG chiên dầu, KHÔNG chất bảo quản, KHÔNG thêm đường tinh luyện.\n"
        "- Tiêu chuẩn FEFO & Truy xuất nguồn gốc: Mỗi túi đều có mã Lô in trên bao bì. Khách có thể nhập mã lô tại trang 'Truy xuất' trên web để kiểm tra vùng trồng VietGAP và hạn dùng.\n"
        "- Chính sách Freeship: Miễn phí vận chuyển toàn quốc cho đơn từ 500.000đ. Phí ship nội thành 22.000đ, tỉnh khác 35.000đ.\n"
        "- Thanh toán: Hỗ trợ COD (tiền mặt khi nhận hàng) và Chuyển khoản ngân hàng VietQR Napas 24/7 (Vietcombank).\n"
        "- Đổi trả: Trong vòng 7 ngày nếu sản phẩm lỗi, bể vỡ do vận chuyển hoặc không đúng cam kết.\n"
        "DANH MỤC SẢN PHẨM HIỆN CÓ:\n" + "\n".join(products_info) + "\n"
        "QUY TẮC QUAN TRỌNG:\n"
        "1. Luôn ưu tiên trả lời về hương vị, thành phần, lợi ích sức khỏe và gợi ý sản phẩm phù hợp.\n"
        "2. Nếu khách hỏi mua số lượng lớn làm quà doanh nghiệp, khiếu nại gay gắt, hoặc yêu cầu gặp người thật, hãy nhã nhặn đề xuất kết nối với tư vấn viên.\n"
        "3. Trả lời bằng tiếng Việt gãy gọn, không dài dòng."
    )


def _rule_based_fallback(user_msg: str) -> dict:
    """Hệ thống phản hồi thông minh dựa trên tri thức NutriSnack khi không có API Key."""
    msg = user_msg.lower()

    # 1. Chào hỏi
    if any(w in msg for w in ["chào", "hello", "hi ", "bạn là ai", "shop ơi", "alo"]):
        return {
            "reply": (
                "Dạ chào bạn! Mình là **NutriBot** - Trợ lý AI của NutriSnack 🌿\n\n"
                "Mình có thể giúp bạn giải đáp về:\n"
                "• Hương vị & thành phần các loại trái cây sấy thăng hoa (Sầu riêng, Dâu tây, Xoài, Mít...)\n"
                "• Hạt dinh dưỡng cao cấp & Granola ăn kiêng, eat clean\n"
                "• Công nghệ sấy thăng hoa -40°C & Truy xuất nguồn gốc lô hàng\n"
                "• Chính sách phí ship và ưu đãi Freeship\n\n"
                "Bạn đang quan tâm đến sản phẩm hoặc hương vị nào ạ?"
            ),
            "is_handoff": False,
            "suggestions": [
                "🍓 Dâu tây sấy ăn thế nào?",
                "Durian sầu riêng sấy có ngọt không?",
                "🥗 Sản phẩm nào ăn kiêng / giảm cân?",
                "🚚 Chính sách Freeship?"
            ]
        }

    # 2. Sầu riêng sấy
    if any(w in msg for w in ["sầu riêng", "sau rieng", "durian"]):
        return {
            "reply": (
                "Dạ **Sầu riêng sấy thăng hoa NutriSnack** được làm từ 100% cơm sầu riêng tươi chín tự nhiên "
                "(giống Ri6 / Monthong tuyển chọn) ạ! 💛\n\n"
                "• **Hương vị:** Thơm nồng nàn, vị ngọt béo tự nhiên đậm đà, hoàn toàn KHÔNG thêm đường.\n"
                "• **Cấu trúc:** Nhờ sấy thăng hoa âm sâu -40°C nên từng múi sầu riêng giữ nguyên thớ thịt, "
                "khi cắn vào giòn xốp và tan êm trong miệng.\n"
                "• **Quy cách:** Túi zip tiện lợi 50g (89.000đ) - thích hợp mang đi làm hoặc biếu tặng.\n\n"
                "Bạn có muốn mình thêm sầu riêng sấy vào giỏ hàng giúp bạn không ạ?"
            ),
            "is_handoff": False,
            "suggestions": ["Thêm vào giỏ hàng", "🍓 Dâu tây sấy thăng hoa", "🥭 Xoài sấy thăng hoa", "🚚 Phí vận chuyển"]
        }

    # 3. Dâu tây sấy
    if any(w in msg for w in ["dâu tây", "dau tay", "strawberry"]):
        return {
            "reply": (
                "Dạ **Dâu tây sấy thăng hoa Đà Lạt** là sản phẩm best-seller của NutriSnack đó ạ! 🍓\n\n"
                "• **Đặc điểm:** Tuyển chọn từ những trái dâu tây tươi mọng nước chuẩn VietGAP tại Đà Lạt. "
                "Sấy thăng hoa nguyên quả, giữ nguyên màu đỏ tươi bắt mắt.\n"
                "• **Hương vị:** Vị chua chua ngọt thanh tự nhiên, giòn rụm sảng khoái, không hề ngọt gắt.\n"
                "• **Công dụng:** Rất giàu Vitamin C và chất chống oxy hóa, rất hợp ăn vặt healthy hoặc ăn kèm sữa chua, yến mạch.\n"
                "• **Giá:** Túi 50g chỉ 65.000đ."
            ),
            "is_handoff": False,
            "suggestions": ["🥭 Xoài sấy thăng hoa", "🥗 Granola ăn kiêng", "🚚 Phí vận chuyển"]
        }

    # 4. Xoài, mít, chuối, thanh long
    if any(w in msg for w in ["xoài", "xoai", "mít", "mit", "chuối", "chuoi", "thanh long"]):
        return {
            "reply": (
                "Dạ các dòng **Trái cây nhiệt đới sấy thăng hoa** của NutriSnack đều cam kết 100% tự nhiên ạ: 🥭🍌\n\n"
                "• **Xoài Cát Chu sấy:** Chua ngọt hài hòa, thơm ngát, túi 50g (48.000đ).\n"
                "• **Mít sấy thăng hoa:** Múi mít dày, thơm giòn đậm vị, túi 50g (45.000đ).\n"
                "• **Chuối sấy thăng hoa:** Giàu Kali, vị ngọt dịu nhẹ, túi 60g (35.000đ).\n"
                "• **Thanh long ruột đỏ:** Giòn xốp, giàu chất xơ & anthocyanin, túi 50g (42.000đ).\n\n"
                "Tất cả đều sấy không dầu, không thêm đường, an toàn cho cả trẻ nhỏ và người lớn tuổi ạ!"
            ),
            "is_handoff": False,
            "suggestions": ["Xem danh sách sản phẩm", "Chính sách freeship", "Hạt dinh dưỡng"]
        }

    # 5. Ăn kiêng, giảm cân, eat clean, tiểu đường, gym
    if any(w in msg for w in ["ăn kiêng", "an kieng", "giảm cân", "giam can", "tiểu đường", "tieu duong", "eat clean", "gym", "healthy"]):
        return {
            "reply": (
                "Dạ nếu bạn đang theo chế độ **Eat Clean, Giảm cân hoặc Kiểm soát đường huyết**, "
                "NutriSnack gợi ý cho bạn 3 lựa chọn lý tưởng nhất:\n\n"
                "1. **Granola siêu hạt không đường:** Yến mạch nướng giòn kết hợp hạnh nhân, hạt điều, hạt bí và nho khô. "
                "Giàu protein và chất xơ, tạo cảm giác no lâu (Hũ 500g: 135.000đ).\n"
                "2. **Daily Trail Mix 7 ngày:** Từng gói 35g chia sẵn calo chuẩn mực cho bữa phụ hoặc trước tập gym (Combo 7 ngày: 105.000đ).\n"
                "3. **Hạt Macca & Hạnh nhân rang bơ:** Giàu chất béo tốt Omega-3, không làm tăng đường huyết.\n"
                "4. **Dâu tây / Thanh long sấy:** Lượng calo cực thấp, hoàn toàn không thêm đường tinh luyện."
            ),
            "is_handoff": False,
            "suggestions": ["Granola siêu hạt", "Hạt Macca Đắk Lắk", "Gặp nhân viên tư vấn"]
        }

    # 6. Công nghệ sấy thăng hoa là gì?
    if any(w in msg for w in ["sấy thăng hoa", "say thang hoa", "freeze dry", "freeze-dry", "công nghệ"]):
        return {
            "reply": (
                "Dạ **Sấy thăng hoa (Freeze-Drying)** là công nghệ sấy thực phẩm tiên tiến nhất hiện nay ạ: ❄️🔬\n\n"
                "1. **Cơ chế:** Trái cây tươi được cấp đông âm sâu ở nhiệt độ **-40°C**, sau đó đưa vào buồng hút chân không. "
                "Tại đây, tinh thể nước đá thăng hoa trực tiếp từ thể rắn sang thể khí mà không qua thể lỏng.\n"
                "2. **Khác biệt vượt trội:**\n"
                "   • Khác với sấy nhiệt (bị teo tóp, mất chất do nhiệt cao) hay sấy dẻo (thường tẩm nhiều đường).\n"
                "   • Sấy thăng hoa giữ nguyên **95% vitamin**, hình dáng múi quả nguyên vẹn, màu sắc tươi tắn và cấu trúc giòn xốp tan trong miệng.\n"
                "   • Hoàn toàn không chiên dầu, không chất bảo quản."
            ),
            "is_handoff": False,
            "suggestions": ["🍓 Thử Dâu tây sấy", "Durian Sầu riêng sấy", "Tra cứu nguồn gốc lô hàng"]
        }

    # 7. Phí vận chuyển, freeship, thời gian giao hàng
    if any(w in msg for w in ["ship", "vận chuyển", "freeship", "bao lâu", "giao hàng", "phí"]):
        threshold = getattr(settings, "FREE_SHIPPING_THRESHOLD", 500000)
        urban_fee = getattr(settings, "SHIPPING_FEE_URBAN", 22000)
        other_fee = getattr(settings, "SHIPPING_FEE_OTHER", 35000)
        return {
            "reply": (
                f"Dạ chính sách vận chuyển của NutriSnack rất rõ ràng và ưu đãi ạ: 🚚\n\n"
                f"• 🎉 **FREESHIP TOÀN QUỐC:** Cho mọi đơn hàng từ **{threshold:,}đ** trở lên!\n"
                f"• **Nội thành TP.HCM / Hà Nội:** {urban_fee:,}đ (Giao hỏa tốc 1 - 2 ngày làm việc).\n"
                f"• **Tỉnh thành khác:** {other_fee:,}đ (Giao tận nơi qua chuyển phát nhanh 2 - 4 ngày).\n"
                f"• Bạn được kiểm tra hàng trước khi thanh toán (COD) hoặc quét VietQR tiện lợi!"
            ),
            "is_handoff": False,
            "suggestions": ["Xem giỏ hàng", "Danh mục sản phẩm", "Gặp tư vấn viên"]
        }

    # 8. Truy xuất nguồn gốc, lô hàng, hạn dùng, FEFO
    if any(w in msg for w in ["lô hàng", "lo hang", "truy xuất", "truy xuat", "hạn dùng", "hsd", "fefo"]):
        return {
            "reply": (
                "Dạ tại NutriSnack, 100% sản phẩm đều tuân thủ nguyên tắc **Minh bạch nguồn gốc & Tiêu chuẩn FEFO**: 🔍\n\n"
                "• **Mã lô in trên bao bì:** Mỗi gói sản phẩm đều có mã lô riêng (ví dụ: `LOT-SR2601`).\n"
                "• **Tra cứu trực tuyến:** Bạn chỉ cần bấm vào mục **'Truy xuất nguồn gốc'** trên menu đầu trang web, "
                "nhập mã lô để xem ngày sản xuất, hạn sử dụng và chứng nhận VietGAP của vùng trồng.\n"
                "• **Cam kết hạn dùng:** Shop chỉ xuất kho các lô hàng có hạn sử dụng từ 30 ngày trở lên, tuyệt đối không bán hàng cận hạn!"
            ),
            "is_handoff": False,
            "suggestions": ["Đến trang Truy xuất", "Chính sách đổi trả", "Xem sản phẩm"]
        }

    # 9. Mặc định: Trả lời lịch sự và gợi ý gặp người thật nếu chưa đúng ý
    return {
        "reply": (
            "Dạ mình đã ghi nhận câu hỏi của bạn! Vì là trợ lý ảo AI, mình chuyên giải đáp thông tin về "
            "sản phẩm trái cây sấy thăng hoa, hạt dinh dưỡng, công nghệ chế biến và chính sách giao hàng của shop 🌿\n\n"
            "Nếu bạn cần giải đáp chuyên sâu hơn hoặc hỗ trợ riêng, mình có thể kết nối ngay với **Tư vấn viên người thật** giúp bạn nhé!"
        ),
        "is_handoff": False,
        "suggestions": [
            "👨‍💼 Gặp tư vấn viên người thật",
            "🍓 Tư vấn hương vị trái cây sấy",
            "🥗 Sản phẩm ăn kiêng healthy",
            "🚚 Chính sách Freeship 500k"
        ]
    }


def get_chat_response(message: str, history: list = None) -> dict:
    """Hàm xử lý tin nhắn chính: Phân loại Handoff -> Gọi Gemini AI -> Dự phòng Rule-based."""
    message = (message or "").strip()
    if not message:
        return {
            "reply": "Dạ bạn có câu hỏi nào về sản phẩm hoặc hương vị của NutriSnack không ạ?",
            "is_handoff": False,
            "suggestions": []
        }

    # BƯỚC 1: Kiểm tra xem có kích hoạt luồng chuyển giao người thật không
    if check_handoff_trigger(message):
        return get_handoff_response()

    # BƯỚC 2: Kiểm tra nếu có cấu hình GEMINI_API_KEY thì gọi Google Gemini API
    gemini_key = getattr(settings, "GEMINI_API_KEY", "")
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            system_prompt = _build_system_context()

            # Chuẩn bị contents
            contents = [
                {"role": "user", "parts": [{"text": system_prompt}]},
                {"role": "model", "parts": [{"text": "Dạ vâng, tôi đã nắm rõ toàn bộ thông tin sản phẩm và chính sách của NutriSnack. Tôi sẵn sàng hỗ trợ khách hàng chu đáo và thân thiện nhất!"}]}
            ]

            if history and isinstance(history, list):
                for h in history[-4:]:
                    role = "user" if h.get("sender") == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": h.get("text", "")}]})

            contents.append({"role": "user", "parts": [{"text": message}]})

            resp = requests.post(
                url,
                json={"contents": contents, "generationConfig": {"temperature": 0.4, "maxOutputTokens": 600}},
                timeout=6
            )
            if resp.status_code == 200:
                data = resp.json()
                reply_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                # Kiểm tra nếu câu trả lời của AI có ý định cần gặp nhân viên
                is_handoff = check_handoff_trigger(reply_text)
                return {
                    "reply": reply_text,
                    "is_handoff": is_handoff,
                    "handoff_info": get_handoff_response()["handoff_info"] if is_handoff else None,
                    "suggestions": ["Sầu riêng sấy có ngọt không?", "Sản phẩm ăn kiêng", "Phí vận chuyển", "Gặp tư vấn viên"]
                }
        except Exception as e:
            logger.warning("Lỗi gọi Gemini API, chuyển sang Rule-based Engine: %s", e)

    # BƯỚC 3: Dự phòng bằng Rule-based Knowledge Engine
    return _rule_based_fallback(message)

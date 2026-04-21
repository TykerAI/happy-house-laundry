#!/usr/bin/env python3
"""
Happy House Laundry - Documentation Translation Build Script (Optimized)
This script reads the Vietnamese `index.html`, injects missing selector
assets if necessary, processes site translations into English, 
and generates the `en.html` file seamlessly.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Tuple

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

SOURCE_FILE = Path('index.html')
TARGET_FILE = Path('en.html')

# -----------------------------------------------------------------------------
# Asset Injection Constants (Used as fallbacks)
# -----------------------------------------------------------------------------
LANG_SELECTOR_CSS_MARKER = '/* ============================================================'
LANG_SELECTOR_CSS_TO_ADD = """
        /* ============================================================
           LANGUAGE SELECTOR
           ============================================================ */
        .lang-selector {
            position: relative;
            margin-left: 0.5rem;
        }

        .lang-btn {
            background: transparent;
            border: 1px solid var(--border-medium);
            padding: 0.4rem 0.8rem;
            border-radius: 8px;
            font-family: var(--font-body);
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-primary);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.4rem;
            transition: all 0.25s;
        }

        .lang-btn:hover {
            border-color: var(--gold-500);
            background: var(--gold-100);
        }

        .lang-btn .flag {
            font-size: 1.1rem;
        }

        .lang-menu {
            position: absolute;
            top: calc(100% + 10px);
            right: 0;
            background: var(--white);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            list-style: none;
            min-width: 130px;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 100;
        }

        .lang-selector:hover .lang-menu,
        .lang-menu.show {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }

        .lang-menu a {
            display: flex !important;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1rem !important;
            color: var(--text-secondary) !important;
            text-transform: none !important;
            font-weight: 500 !important;
            letter-spacing: normal !important;
            border-radius: 8px;
        }

        .lang-menu a::after {
            display: none !important;
        }

        .lang-menu a:hover {
            background: var(--light-50);
            color: var(--gold-600) !important;
        }
        
        .mobile-lang-switch {
            border-top: 1px solid var(--light-200);
            margin-top: 1rem;
            padding-top: 1rem;
        }
        
        .mobile-lang-switch a {
            display: flex !important;
            align-items: center;
            gap: 0.5rem;
            border-bottom: none !important;
            font-size: 0.95rem !important;
            color: var(--text-primary) !important;
        }
"""

DESKTOP_NAV_SEARCH = '                    <li><a href="tel:0914744333" class="nav-cta"><i class="fas fa-phone-alt"></i> Gọi Ngay</a></li>'
DESKTOP_NAV_REPLACE = """                    <li><a href="tel:0914744333" class="nav-cta"><i class="fas fa-phone-alt"></i> Gọi Ngay</a></li>
                    <li class="lang-selector">
                        <button class="lang-btn" aria-haspopup="true" aria-expanded="false">
                            <span class="flag">🇻🇳</span> Tiếng Việt <i class="fas fa-chevron-down" style="font-size:0.7rem; margin-left:2px;"></i>
                        </button>
                        <ul class="lang-menu">
                            <li><a href="en.html"><span class="flag" style="font-size:1.2rem;">🇺🇸</span> English</a></li>
                        </ul>
                    </li>"""

MOBILE_NAV_SEARCH = '            <a href="tel:0914744333" class="mobile-cta"><i class="fas fa-phone-alt"></i> Gọi Ngay: 0914 744 333</a>'
MOBILE_NAV_REPLACE = """            <a href="tel:0914744333" class="mobile-cta"><i class="fas fa-phone-alt"></i> Gọi Ngay: 0914 744 333</a>
            <div class="mobile-lang-switch">
                <a href="en.html"><span class="flag" style="font-size:1.2rem;">🇺🇸</span> Switch to English</a>
            </div>"""

# -----------------------------------------------------------------------------
# Translations Dict
# -----------------------------------------------------------------------------
TRANSLATIONS: Dict[str, str] = {
    # Head and SEO
    "Happy House Laundry — Giặt Sấy Chuyên Nghiệp Đà Nẵng": "Happy House Laundry — Premium Laundry Services Da Nang",
    "Dịch vụ giặt sấy chuyên nghiệp hàng đầu Đà Nẵng. Giao nhận tận nơi, thiết bị hiện đại, cam kết chất lượng 100%.": "Da Nang's leading premium laundry service. Door-to-door delivery, modern equipment, 100% quality guarantee.",
    'lang="vi"': 'lang="en"',
    
    # Lang switcher update for en.html
    '<img src="https://flagcdn.com/w20/vn.png" srcset="https://flagcdn.com/w40/vn.png 2x" alt="VN" class="flag"> Tiếng Việt <i class="fas fa-chevron-down" style="font-size:0.7rem; margin-left:2px; color: var(--dark-800);"></i>': '<img src="https://flagcdn.com/w20/us.png" srcset="https://flagcdn.com/w40/us.png 2x" alt="US" class="flag" style="width:22px; border-radius:2px;"> English <i class="fas fa-chevron-down" style="font-size:0.7rem; margin-left:2px; color: var(--dark-800);"></i>',
    '<li><a href="en.html"><img src="https://flagcdn.com/w20/us.png" srcset="https://flagcdn.com/w40/us.png 2x" alt="US" class="flag" style="width:20px; border-radius:2px;"> English</a></li>': '<li><a href="index.html"><img src="https://flagcdn.com/w20/vn.png" srcset="https://flagcdn.com/w40/vn.png 2x" alt="VN" class="flag" style="width:20px; border-radius:2px;"> Tiếng Việt (Vietnamese)</a></li>',
    '<a href="en.html"><img src="https://flagcdn.com/w20/us.png" alt="US" style="width:22px; border-radius:2px;"> Switch to English</a>': '<a href="index.html"><img src="https://flagcdn.com/w20/vn.png" alt="VN" style="width:22px; border-radius:2px;"> Đổi sang Tiếng Việt</a>',
    
    # Top bar
    "Thứ Hai – Chủ Nhật": "Monday – Sunday",
    
    # Navbar
    "Trang Chủ": "Home",
    "Dịch Vụ": "Services",
    "Ưu Điểm": "Why Us",
    "Quy Trình": "Process",
    "Liên Hệ": "Contact",
    "Gọi Ngay": "Call Now",
    "Gọi Ngay: ": "Call Now: ",
    "Menu di động": "Mobile menu",
    
    # Hero
    "Năm<br>Kinh Nghiệm": "Years of<br>Experience",
    "Dịch vụ giặt ủi Đà Nẵng": "Premium Da Nang Laundry",
    "Giặt Sấy<br>\n                        Chuyên Nghiệp<br>": "Professional<br>\n                        Laundry Care<br>",
    "Từ một tiệm giặt truyền thống, Happy House Laundry vươn mình trở thành\n                        mô hình giặt ủi thông minh hàng đầu Đà Nẵng — mang đến dịch vụ\n                        <strong style=\"color: var(--text-primary);\">lấy & trả tận nơi</strong>,\n                        thiết bị công nghệ cao, và cam kết không vết bẩn 100%.": "Evolving from a traditional shop, Happy House Laundry is now Da Nang's leading smart laundry model. We deliver <strong style=\"color: var(--text-primary);\">door-to-door convenience</strong>, high-tech imported equipment, and a 100% spotless guarantee.",
    "Giá cả cạnh tranh — minh bạch, không phát sinh": "Competitive, crystal-clear pricing — zero hidden fees",
    "Giao nhận tận nơi siêu tốc trong nội thành": "Express door-to-door delivery within the city",
    "Thiết bị thông minh chuẩn quốc tế": "International standard smart machinery",
    "Cam kết xử lý lại miễn phí nếu không hài lòng": "100% Satisfaction: Free re-wash guarantee",
    "Đặt Lịch Ngay": "Book Now",
    "Khám Phá Dịch Vụ": "Explore Services",
    
    # Trust Strip
    "Đánh Giá 5 Sao": "5-Star Reviews",
    "Năm Kinh Nghiệm": "Years Experience",
    "Khách Hàng Hài Lòng": "Happy Customers",
    "Cam Kết Chất Lượng": "Quality Guarantee",
    
    # Three Pillars
    "Cam Kết Của Chúng Tôi": "Our Commitment",
    "Ba Trụ Cột <span class=\"gold\">Chất Lượng</span>": "Three Pillars of <span class=\"gold\">Quality</span>",
    "Mỗi chiếc áo bạn trao cho chúng tôi đều được chăm sóc bằng quy trình chuẩn mực cao nhất.": "Every garment you entrust to us is meticulously cared for using the highest industry standards.",
    "Chất Lượng Cao Cấp": "Premium Quality",
    "Quy trình chuyên nghiệp, khắt khe đến từng chi tiết. Quần áo được trả lại\n                        sạch tinh khôi, giữ trọn form dáng và màu sắc ban đầu.": "Rigorous, professional processing down to the finest detail. Clothes are returned immaculately clean, retaining their original shape and vibrant colors.",
    "Sạch & Thân Thiện Môi Trường": "Eco-Friendly & Safe",
    "Dung môi an toàn cho da và sức khỏe, thân thiện với môi trường. Tiết kiệm\n                        năng lượng tối đa nhờ công nghệ vận hành 4.0 thông minh.": "We use premium solvents that are safe for your skin and the environment, powered by energy-efficient 4.0 smart technology.",
    "Bảo Hành Niềm Tin": "The Trust Guarantee",
    "Hơn 200+ đánh giá 5 sao từ khách hàng thực. Xử lý lại hoàn toàn miễn phí nếu\n                        bạn chưa hài lòng — lấy uy tín làm cốt lõi.": "Backed by hundreds of genuine 5-star reviews. We offer completely free re-processing if you are not fully satisfied — trust is our core.",
    
    # Services
    "Hệ Sinh Thái Dịch Vụ": "Our Service Ecosystem",
    "Dịch Vụ Tại <span class=\"gold\">Happy House Laundry</span>": "Services at <span class=\"gold\">Happy House Laundry</span>",
    "Toàn bộ dịch vụ giặt sấy từ cá nhân đến thương mại, được thực hiện bởi đội ngũ chuyên nghiệp với\n                    thiết bị hiện đại.": "Comprehensive laundry solutions from personal to commercial, executed by a professional team with state-of-the-art equipment.",
    
    "Giặt Đồ Khách Sạn": "Hospitality Laundry",
    "Xử lý khối lượng lớn, đúng tiến độ — đảm bảo tiêu chuẩn vệ sinh\n                            hospitality.": "Expertly handling large commercial volumes on schedule while exceeding strict hospitality hygiene standards.",
    "Giặt Sấy Cá Nhân": "Personal Wash & Fold",
    "Dịch vụ giao nhận tận nơi, giặt theo trọng lượng, phù hợp mọi gia\n                            đình.": "Convenient door-to-door delivery, weight-based washing tailored perfectly for busy individuals and families.",
    "Giặt Khô Cao Cấp": "Premium Dry Cleaning",
    "Xử lý vải đặc biệt, hàng hiệu, vest, áo khoác với quy trình chuyên\n                            biệt.": "Specialized care for delicate fabrics, designer brands, bespoke suits, and heavy coats.",
    "Giặt Rèm & Sofa": "Curtain & Sofa Cleaning",
    "Vệ sinh rèm cửa, nệm sofa chuyên sâu, khử khuẩn 99.9%.": "Deep cleaning and 99.9% antibacterial sanitization for curtains, carpets, and sofa mattresses.",
    "Spa Giày Sneaker": "Premium Sneaker Spa",
    "Vệ sinh, phục hồi giày chuyên sâu — từ sneaker phổ thông đến hàng\n                            hiệu.": "Deep cleaning and meticulous restoration for all footwear — from everyday sneakers to luxury brands.",
    "Giặt Công Nghiệp": "Commercial Laundry",
    "Giải pháp giặt ủi cho nhà máy, bệnh viện, spa — số lượng lớn, chu kỳ\n                            nhanh.": "Industrial solutions for factories, hospitals, and spas featuring fast turnarounds for massive volumes.",
    
    # Why Choose Us
    "Điểm Khác Biệt": "Our Differentiators",
    "Tại Sao Chọn <span class=\"gold\">Happy House?</span>": "Why Choose <span class=\"gold\">Happy House?</span>",
    "6 ưu điểm vượt trội giúp chúng tôi tự tin là lựa chọn hàng đầu của hàng trăm gia đình Đà Nẵng.": "6 outstanding advantages that make us the undisputed top choice for hundreds of families and expats in Da Nang.",
    
    "Hãy đến với<br><span style=\"color: var(--gold-500);\">Happy House Laundry</span>": "Experience the Best with<br><span style=\"color: var(--gold-500);\">Happy House</span>",
    "Giặt sạch hơn, nhanh hơn,<br>và bền vững hơn mỗi ngày": "Cleaner, faster,<br>and more sustainable every day",
    
    "Dung Môi Nhập Khẩu": "Imported Premium Solvents",
    "Nước giặt xả chuẩn quốc tế, bảo vệ cấu trúc vải an toàn.": "International-grade detergents that deeply clean while safely protecting delicate fabric structures.",
    "Phục Vụ Tận Tâm": "Dedicated Customer Care",
    "Giao tiếp thân thiện, rõ ràng, khách hàng là trung tâm.": "Friendly, English-speaking staff providing clear communication and customer-centric service.",
    "Giặt ủi bằng công nghệ Nhật": "Japanese Technology",
    "Máy móc hiện đại, cảm biến thông minh với nhiều tính năng ưu việt.": "Cutting-edge modern machinery equipped with smart sensors for superior garment care.",
    "Tối Ưu Thời Gian": "Time Optimization",
    "Giải phóng thời gian, dành công sức cho việc quan trọng hơn.": "Free up your valuable time so you can focus on things that matter more to you.",
    "Lọc Nước Tinh Khiết": "Pure Water Filtration",
    "Xử lý nước cứng trước khi giặt, đồ trắng sáng đẹp hơn.": "Advanced hard water treatment before every cycle ensures your whites stay bright and brilliant.",
    "Giao nhận tận nơi và tận tình": "Dedicated Door-to-Door Delivery",
    "Lấy và trả đúng hẹn, theo dõi lộ trình di chuyển sát sao.": "Punctual pick-up and delivery right to your hotel or home, with close tracking.",
    
    # Process
    "Quy Trình Đặt Dịch Vụ": "How It Works",
    "Chỉ <span class=\"gold\">4 Bước</span> Đơn Giản": "Just <span class=\"gold\">4 Simple Steps</span>",
    "Từ lúc đặt lịch đến khi nhận đồ sạch — mọi thứ diễn ra mượt mà và minh bạch.": "From intuitive booking to receiving your fresh clothes — everything is smooth, fast, and completely transparent.",
    
    "Đặt Lịch": "Book Your Service",
    "Gọi điện hoặc nhắn tin qua Zalo / Facebook để đặt lịch lấy đồ.": "Simply call or message us via Zalo, WhatsApp, or Facebook to schedule a convenient pick-up.",
    "Lấy Đồ Tận Nơi": "We Pick It Up",
    "Chúng tôi đến tận nhà, kiểm đếm và ghi nhận tình trạng đồ cho bạn.": "Our staff arrives at your location, carefully counts, and notes the precise condition of your items.",
    "Giặt & Sấy": "Expert Processing",
    "Quy trình xử lý chuyên nghiệp theo từng loại vải, đảm bảo sạch 100%.": "Items are sorted and processed using specialized methods per fabric type, guaranteeing 100% cleanliness.",
    "Giao Tận Tay": "Delivered to You",
    "Đồ được giao lại thơm tho, gọn gàng đúng hẹn — thanh toán linh hoạt.": "Your clothes are returned fresh, neatly folded, and right on time — with flexible payment options.",
    
    # Banner
    "Sẵn Sàng Trải Nghiệm<br><span\n                        style=\"color: var(--white); text-shadow: 0 2px 5px rgba(0,0,0,0.15);\">Dịch Vụ Của Chúng\n                        Tôi?</span>": "Ready to Experience<br><span\n                        style=\"color: var(--white); text-shadow: 0 2px 5px rgba(0,0,0,0.15);\">Our Premium Services?</span>",
    "Hơn 1000 gia đình tại Đà Nẵng đã tin tưởng Happy House Laundry.<br>Hãy để chúng tôi chăm sóc tủ đồ của\n                    bạn ngay hôm nay.": "Over 1,000 families and expats in Da Nang trust Happy House Laundry.<br>Let us take care of your wardrobe starting today.",
    "Nhắn Qua Zalo": "Message via Zalo",
    
    # Contact
    "Tìm Chúng Tôi": "Locate Us",
    "Địa Chỉ & <span class=\"gold\">Liên Hệ</span>": "Address & <span class=\"gold\">Contact</span>",
    "Thông Tin Cửa Hàng": "Our Store Information",
    "Địa Chỉ": "Address",
    "Giờ Mở Cửa": "Opening Hours",
    "Thứ Hai – Chủ Nhật": "Mon – Sun",
    "Chủ Quản": "Business Owner",
    
    "HỘ KINH DOANH HAPPY HOUSE": "HAPPY HOUSE BUSINESS HOUSEHOLD",
    "Gọi Ngay Đặt Lịch": "Call Now to Book",
    
    # Footer
    "Dịch vụ giặt sấy chuyên nghiệp hàng đầu Đà Nẵng — mang đến sự sạch sẽ, tiện lợi và niềm tin\n                        tuyệt đối cho mọi gia đình.": "Da Nang's premier premium laundry service — delivering exceptional cleanliness, unrivaled convenience, and absolute trust for every household.",
    "Hệ Sinh Thái Dịch Vụ": "Service Ecosystem",
    "Giặt sấy tự động hóa": "Automated Wash & Fold",
    "Xử lý đồ vải công nghiệp": "Commercial Linen Processing",
    "Giặt rèm cửa, nệm sofa": "Curtains & Sofa Deep Cleaning",
    "Spa giày Sneaker chuyên sâu": "Premium Sneaker Spa & Care",
    "Tẩy điểm bẩn, phục hồi màu vải": "Advanced Stain Removal",
    "Nhượng quyền thương hiệu": "Franchise Opportunities",
    
    "Chính Sách & Liên Kết": "Policies & Quick Links",
    "Điều khoản bảo mật thông tin": "Privacy Policy",
    "Chính sách bồi thường, xử lý lỗi": "Compensation & Claims Policy",
    "Trụ sở chính: 155 Hải Sơn": "Headquarters: 155 Hai Son",
    "Thiết kế bởi Châu Anh Dũng.": "Designed by Chau Anh Dung.",
    
    "Cuộn lên đầu trang": "Scroll to top",
    
    # Specific edge cases
    "155 Hải Sơn, Hải Châu, TP. Đà Nẵng": "155 Hai Son, Hai Chau District, Da Nang City",
    "155 Hải Sơn, Hải Châu, Đà Nẵng": "155 Hai Son, Hai Chau Dist, Da Nang",
}

# -----------------------------------------------------------------------------
# Main Translation Engine Class
# -----------------------------------------------------------------------------
class SiteTranslator:
    def __init__(self, source: Path, target: Path):
        self.source = source
        self.target = target
        self.content = ""

    def load_source(self) -> bool:
        """Reads the source HTML file into memory."""
        if not self.source.exists():
            logging.error(f"Source file '{self.source}' not found. Cannot proceed.")
            return False
            
        logging.info(f"Loaded source file: {self.source}")
        self.content = self.source.read_text(encoding='utf-8')
        return True
        
    def inject_components(self) -> None:
        """Injects missing language selector code into index.html if absent."""
        changes_made = False
        
        # Inject CSS
        if '.lang-selector {' not in self.content:
            logging.info("Missing '.lang-selector' CSS. Injecting styles into index.html.")
            self.content = self.content.replace(
                LANG_SELECTOR_CSS_MARKER, 
                LANG_SELECTOR_CSS_TO_ADD + '\\n        ' + LANG_SELECTOR_CSS_MARKER, 
                1
            )
            changes_made = True

        # Inject Desktop Nav
        if 'class="lang-selector"' not in self.content:
            logging.info("Missing desktop '.lang-selector'. Injecting HTML into index.html.")
            self.content = self.content.replace(DESKTOP_NAV_SEARCH, DESKTOP_NAV_REPLACE)
            changes_made = True

        # Inject Mobile Nav
        if 'class="mobile-lang-switch"' not in self.content:
            logging.info("Missing mobile '.mobile-lang-switch'. Injecting HTML into index.html.")
            self.content = self.content.replace(MOBILE_NAV_SEARCH, MOBILE_NAV_REPLACE)
            changes_made = True

        if changes_made:
            self.source.write_text(self.content, encoding='utf-8')
            logging.info(f"Saved injected components back to {self.source}")
        else:
            logging.info("All language selector components are already intact in index.html.")

    def build_english_version(self) -> None:
        """Creates the structural clone and performs content translation for en.html."""
        logging.info("Beginning English translation map building...")
        en_content = self.content

        # Handle text translations
        missing_keys = []
        for vi_text, en_text in TRANSLATIONS.items():
            if vi_text not in en_content:
                missing_keys.append(vi_text[:40])
            en_content = en_content.replace(vi_text, en_text)

        if missing_keys:
            logging.warning(f"Translation replaced, but missed {len(missing_keys)} exact keys (content might be altered in index.html):")
            for key in missing_keys[:5]:
                logging.warning(f"  - '{key}...'")

        # Specific replacement for changing map localization UI to English
        en_content = en_content.replace('!1svi!2s', '!1sen!2s')

        # Write output
        self.target.write_text(en_content, encoding='utf-8')
        logging.info(f"Success: English version written perfectly to '{self.target}'!")

# -----------------------------------------------------------------------------
# Script Entry Point
# -----------------------------------------------------------------------------
def main() -> None:
    logging.info("=========================================")
    logging.info("    Happy House - Build Translator       ")
    logging.info("=========================================")
    
    translator = SiteTranslator(SOURCE_FILE, TARGET_FILE)
    
    if translator.load_source():
        translator.inject_components()
        translator.build_english_version()
        
    logging.info("=========================================")

if __name__ == "__main__":
    main()

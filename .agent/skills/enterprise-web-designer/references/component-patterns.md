# Component Patterns — HTML/CSS Chuẩn

## Hero Section (Full Screen)
```html
<section class="hero">
  <div class="hero__bg"></div>
  <div class="container hero__content">
    <span class="hero__badge">✦ Thương hiệu uy tín từ 2018</span>
    <h1 class="hero__title">Headline mạnh, ngắn,<br>có hook ngay</h1>
    <p class="hero__sub">Mô tả giá trị cốt lõi trong 1-2 câu. Cụ thể, không chung chung.</p>
    <div class="hero__actions">
      <a href="#contact" class="btn btn--primary">Đặt lịch ngay →</a>
      <a href="#services" class="btn btn--ghost">Xem dịch vụ</a>
    </div>
  </div>
  <div class="hero__scroll-hint">↓</div>
</section>
```

```css
.hero {
  min-height: 100svh;
  display: grid;
  place-items: center;
  position: relative;
  overflow: hidden;
}
.hero__content { 
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 800px;
}
.hero__title {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 6vw, 5rem);
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 1.5rem;
}
.hero__sub {
  font-size: clamp(1rem, 2vw, 1.25rem);
  opacity: 0.75;
  max-width: 560px;
  margin: 0 auto 2rem;
  line-height: 1.6;
}
```

## Stats / Social Proof Row
```html
<section class="stats">
  <div class="container stats__grid">
    <div class="stat-item">
      <span class="stat-number">500+</span>
      <span class="stat-label">Khách hàng hài lòng</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item">
      <span class="stat-number">5★</span>
      <span class="stat-label">Đánh giá trung bình</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item">
      <span class="stat-number">6 năm</span>
      <span class="stat-label">Kinh nghiệm phục vụ</span>
    </div>
  </div>
</section>
```

## Service Cards
```html
<section class="services" id="services">
  <div class="container">
    <h2 class="section-title">Dịch vụ của chúng tôi</h2>
    <div class="services__grid">
      <article class="service-card">
        <div class="service-card__icon">🧺</div>
        <h3 class="service-card__title">Giặt thường</h3>
        <p class="service-card__desc">Mô tả ngắn, rõ lợi ích, không marketing rỗng.</p>
        <span class="service-card__price">Từ 15.000đ/kg</span>
      </article>
    </div>
  </div>
</section>
```

## Testimonial Section
```html
<section class="testimonials">
  <div class="container">
    <h2 class="section-title">Khách hàng nói gì?</h2>
    <div class="testimonials__grid">
      <blockquote class="testimonial-card">
        <div class="stars">★★★★★</div>
        <p>"Nội dung review thật, không sáo rỗng. Cụ thể vấn đề đã giải quyết."</p>
        <cite>
          <img src="avatar.jpg" alt="Nguyễn Thị A" width="40" height="40">
          <span class="cite-name">Nguyễn Thị A</span>
          <span class="cite-title">Khách hàng từ 2022</span>
        </cite>
      </blockquote>
    </div>
  </div>
</section>
```

## CTA Section (Final Conversion)
```html
<section class="cta-final">
  <div class="container cta-final__inner">
    <h2>Sẵn sàng trải nghiệm?</h2>
    <p>Đặt lịch ngay hôm nay — nhận ưu đãi 10% cho đơn đầu tiên.</p>
    <a href="tel:0123456789" class="btn btn--primary btn--large">
      📞 Gọi ngay: 0123 456 789
    </a>
  </div>
</section>
```

## Button Styles
```css
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
  border: 2px solid transparent;
}
.btn--primary {
  background: var(--color-primary);
  color: white;
}
.btn--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}
.btn--ghost {
  background: transparent;
  border-color: currentColor;
  color: var(--color-primary);
}
.btn--large {
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
}
```

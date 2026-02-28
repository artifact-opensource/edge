# Launch Images - README

**Directory:** `/docs/images/launch/`  
**Created:** February 8, 2026  
**Theme:** Monochromic - Sharp White (#FFFFFF) + AMOLED Black (#000000)

---

## 📁 Directory Structure

```
launch/
├── linkedin/
│   └── av-launch-linkedin-hero.svg (1200×627)
├── twitter/
│   └── av-launch-twitter-milestone.svg (1200×675)
├── discord/
│   └── av-launch-discord-announcement.svg (1920×1080)
├── facebook/
│   └── (use LinkedIn or Twitter templates)
├── notion/
│   └── av-launch-notion-cover.svg (1500×600)
├── profile/
│   ├── av-profile-black-bg.svg (512×512)
│   └── av-profile-white-bg.svg (512×512)
└── source/
    └── templates/
```

---

## 🎨 Available SVG Templates

### 1. LinkedIn Hero (1200×627)
**File:** `linkedin/av-launch-linkedin-hero.svg`  
**Theme:** Black background, white text  
**Content:**
- 🚀 Rocket icon
- "ARTIFACT VIRTUAL" main title
- "NOW OPERATIONAL" subtitle
- Tagline about AI/ML infrastructure
- Stats: 18 Projects, 36.5% GRC, $100B+ TAM
- Website URL

**Usage:** LinkedIn post image, primary announcement

---

### 2. Twitter Milestone (1200×675)
**File:** `twitter/av-launch-twitter-milestone.svg`  
**Theme:** White background with black bars  
**Content:**
- Top black bar with brand name
- "MILESTONE 1.0 'GENESIS' ✅ COMPLETED"
- Date and registration number
- Bottom black bar with stats

**Usage:** Twitter card, milestone announcements

---

### 3. Discord Announcement (1920×1080)
**File:** `discord/av-launch-discord-announcement.svg`  
**Theme:** Black background, full HD  
**Content:**
- 🚀 Rocket icon
- "ARTIFACT VIRTUAL Officially Operational"
- 6 key stats in grid format
- Website and GitHub links

**Usage:** Discord embeds, community announcements

---

### 4. Notion Cover (1500×600)
**File:** `notion/av-launch-notion-cover.svg`  
**Theme:** Black background, quote style  
**Content:**
- Inspirational quote about building the future
- Attribution to Artifact Virtual
- "Operational Since February 2026"

**Usage:** Notion page covers, headers

---

### 5. Profile - Black Background (512×512)
**File:** `profile/av-profile-black-bg.svg`  
**Theme:** Square, black circle, white "AV"  
**Content:**
- Simple "AV" monogram
- Bold, minimalist design

**Usage:** Dark mode social media profiles, avatars

---

### 6. Profile - White Background (512×512)
**File:** `profile/av-profile-white-bg.svg`  
**Theme:** Square, white circle, black "AV"  
**Content:**
- Simple "AV" monogram
- Bold, minimalist design

**Usage:** Light mode social media profiles, avatars

---

## 🛠️ How to Use

### Option 1: Use SVG Directly
1. Upload SVG file to social media platform
2. Most platforms support SVG natively
3. Renders at any size without quality loss

### Option 2: Convert to PNG

**Using Inkscape (Command Line):**
```bash
inkscape --export-png=output.png --export-width=1200 input.svg
```

**Using ImageMagick:**
```bash
convert -background none input.svg output.png
```

**Using Online Tools:**
- CloudConvert (https://cloudconvert.com/)
- SVG to PNG Converter
- Figma (import SVG, export PNG)

### Option 3: Edit and Customize
1. Open SVG in text editor or design tool
2. Modify text content, colors, or layout
3. Save and use updated version

---

## 📐 Dimensions Reference

| Platform | Dimension | Aspect Ratio | File |
|----------|-----------|--------------|------|
| **LinkedIn Post** | 1200 × 627 | 1.91:1 | linkedin-hero.svg |
| **Twitter Card** | 1200 × 675 | 16:9 | twitter-milestone.svg |
| **Discord Embed** | 1920 × 1080 | 16:9 | discord-announcement.svg |
| **Facebook Post** | 1200 × 630 | 1.91:1 | Use LinkedIn template |
| **Notion Cover** | 1500 × 600 | 2.5:1 | notion-cover.svg |
| **Profile/Avatar** | 512 × 512 | 1:1 | profile templates |

---

## 🎨 Design Theme

**Colors:**
- Pure Black: `#000000` (RGB: 0, 0, 0)
- Pure White: `#FFFFFF` (RGB: 255, 255, 255)

**Typography:**
- Font Family: Inter, -apple-system, system-ui, sans-serif
- Bold Weights: 700-800 for headlines
- Regular Weights: 400-500 for body text

**Style:**
- Monochromic (black + white only)
- High contrast
- Minimalist
- Modern sans-serif typography
- Clean layouts with white space

---

## ✏️ Customization Guide

### Editing Text Content

1. Open SVG in text editor
2. Find `<text>` elements
3. Edit content between tags:
   ```xml
   <text x="600" y="250">YOUR NEW TEXT</text>
   ```
4. Save and reload

### Changing Colors

Replace hex color values:
- `fill="#000000"` → Black
- `fill="#FFFFFF"` → White

### Adjusting Layout

Modify `x` and `y` coordinates:
- `x`: horizontal position
- `y`: vertical position
- `text-anchor`: alignment (start, middle, end)

---

## 📊 File Sizes

All SVG files are lightweight:
- LinkedIn Hero: ~2KB
- Twitter Milestone: ~2KB
- Discord Announcement: ~3KB
- Notion Cover: ~2KB
- Profile images: <1KB each

**PNG exports will be:**
- LinkedIn (1200×627): ~50-100KB
- Twitter (1200×675): ~50-100KB
- Discord (1920×1080): ~100-200KB
- Notion (1500×600): ~50-100KB
- Profile (512×512): ~20-50KB

---

## 🚀 Quick Start

**For LinkedIn:**
```bash
# Use directly or convert to PNG
cp linkedin/av-launch-linkedin-hero.svg my-linkedin-post.svg
```

**For Twitter:**
```bash
# Convert to PNG for better preview
inkscape --export-png=twitter-card.png --export-width=1200 twitter/av-launch-twitter-milestone.svg
```

**For Discord:**
```bash
# High resolution for embeds
inkscape --export-png=discord-embed.png --export-width=1920 discord/av-launch-discord-announcement.svg
```

**For Profiles:**
```bash
# Convert both variants
inkscape --export-png=profile-black.png --export-width=512 profile/av-profile-black-bg.svg
inkscape --export-png=profile-white.png --export-width=512 profile/av-profile-white-bg.svg
```

---

## 📝 Notes

1. **Font Rendering:** SVGs use system fonts. For consistent rendering across platforms, consider converting to outlines or embedding fonts.

2. **Emoji Support:** Emojis (🚀) may render differently across platforms. Consider replacing with Unicode or custom graphics for consistency.

3. **Accessibility:** All images have high contrast ratios (21:1) exceeding WCAG AAA standards.

4. **Optimization:** SVG files are already optimized. For PNG exports, use compression tools like TinyPNG or ImageOptim.

5. **Variants:** Create additional variants by duplicating and modifying existing templates.

---

## 🔄 Version History

**v1.0 (2026-02-08)**
- Initial creation of 6 SVG templates
- Monochromic theme (black + white)
- Platform-optimized dimensions
- Ready for social media launch

---

## 📞 Support

**Questions?** See parent documentation:
- Main specs: `/docs/LAUNCH-IMAGES-SPECIFICATIONS.md`
- Launch posts: `/docs/LAUNCH-POSTS-README.md`

**Contact:**
- Design: ceo@artifactvirtual.com
- Technical: cto@artifactvirtual.com

---

**All images ready for launch!** 🚀

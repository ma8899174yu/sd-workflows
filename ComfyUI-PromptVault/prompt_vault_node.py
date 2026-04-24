"""
ComfyUI-PromptVault Node
从预设提示词库中加载FLUX/MJ/自然语言提示词
"""

import os
import json
import markdown
from pathlib import Path

# 预设提示词数据库
PRESETS = {
    # ========== FLUX 写实类 ==========
    "flux_portrait_master": {
        "name": "FLUX 人像大师",
        "category": "FLUX/写实",
        "positive": "professional portrait photography, 35mm lens, f/1.8 aperture, soft natural lighting, studio backdrop, subject looking directly at camera, slight smile, confident expression, sharp focus on eyes, skin texture visible, natural skin pores, catch lights in eyes, professional retouching, shallow depth of field, warm skin tones, modern minimalist studio, high-end commercial photography style, 8k resolution, photorealistic, RAW photo quality, color graded, slight vignette",
        "negative": "anime, cartoon, illustration, painting, drawing, sketch, deformed, disfigured, mutated, ugly, bad anatomy, wrong anatomy, extra limbs, missing arms, extra legs, cropped, low resolution, jpeg artifacts, blurry, out of focus, amateur, overexposed, underexposed, watermark, signature, text, logo, frames, border",
        "params": {"steps": "25-35", "cfg": "3.5-5", "sampler": "euler_ancestral / dpmpp_2m", "guidance": "3.5-5"}
    },
    "flux_portrait_corporate": {
        "name": "FLUX 商务人像",
        "category": "FLUX/写实",
        "positive": "professional corporate headshot photography, 85mm lens, f/2.8 aperture, clean studio background, subject wearing business attire, natural smile, confident posture, even lighting on face, sharp focus on face, professional business portrait style, modern corporate branding, high resolution, photorealistic",
        "negative": "anime, cartoon, illustration, painting, casual, informal, deformed, bad anatomy, blurry, low quality, watermark, text",
        "params": {"steps": "20-30", "cfg": "3-4", "sampler": "euler", "guidance": "2-3"}
    },
    "flux_portrait_passport": {
        "name": "FLUX 证件照",
        "category": "FLUX/写实",
        "positive": "official passport photograph, white or light blue background, neutral expression, both eyes visible, natural skin tone, no shadows on face or background, high resolution, biometric passport style, ICAO compliant lighting, professional camera, 50mm lens",
        "negative": "anime, cartoon, illustration, painting, shadows, glasses glare, red-eye, unnatural skin tone, low resolution, watermark",
        "params": {"steps": "15-25", "cfg": "2-3", "sampler": "euler", "guidance": "1.5-2"}
    },
    "flux_cyberpunk_city": {
        "name": "FLUX 赛博朋克城市",
        "category": "FLUX/写实",
        "positive": "cyberpunk cityscape at night, neon signs in Chinese and English, rain-soaked streets, holographic advertisements, flying vehicles, dense urban environment, foggy atmosphere, cinematic lighting, blue and pink neon glow, ultra detailed, 8k resolution, blade runner aesthetic, volumetric fog",
        "negative": "anime, cartoon, illustration, painting, daytime, sunny, simple, low detail, blurry",
        "params": {"steps": "30-40", "cfg": "3.5-5", "sampler": "dpmpp_2m", "guidance": "3-4"}
    },
    "flux_aerial_shanghai": {
        "name": "FLUX 上海航拍",
        "category": "FLUX/写实",
        "positive": "aerial photography of Shanghai skyline at dusk, Pudong skyscrapers, Huangpu River, golden hour lighting, dramatic clouds, city lights beginning to glow, bird's eye view, ultra wide angle, cinematic color grading, 16mm lens, hyperrealistic, 8k resolution",
        "negative": "anime, cartoon, illustration, painting, night time only, cloudy sky, blurry, low quality, distorted perspective",
        "params": {"steps": "28-35", "cfg": "3-4", "sampler": "euler_ancestral", "guidance": "2.5-3.5"}
    },
    "flux_fashion_tokyo": {
        "name": "FLUX 东京时尚街拍",
        "category": "FLUX/写实",
        "positive": "fashion street photography in Tokyo, Omotesando or Shibuya crossing, stylish Japanese models, editorial fashion content, natural candid poses, urban fashion forward style, Leica M10 camera, 35mm lens, natural lighting, magazine cover quality, Vogue editorial style, hyperrealistic",
        "negative": "anime, cartoon, illustration, painting, low quality, blurry, overexposed, amateurish",
        "params": {"steps": "25-32", "cfg": "3-4", "sampler": "dpmpp_2m", "guidance": "2-3"}
    },
    "flux_food_photography": {
        "name": "FLUX 美食摄影",
        "category": "FLUX/写实",
        "positive": "professional food photography, overhead shot, rustic wooden table, natural daylight from window, steam rising from dish, fresh ingredients visible, styled with herbs and garnishes, food blog quality, shallow depth of field, Canon 5D Mark IV, 100mm macro lens, appetizing colors, commercial food photography style",
        "negative": "anime, cartoon, illustration, painting, blurry, overexposed, underexposed, messy plating, low quality",
        "params": {"steps": "20-28", "cfg": "3-4", "sampler": "euler", "guidance": "2-3"}
    },
    "flux_interior_scandinavian": {
        "name": "FLUX 北欧室内",
        "category": "FLUX/写实",
        "positive": "Scandinavian interior design photography, minimalist Copenhagen apartment, white walls, natural wood furniture, plants, hygge atmosphere, soft natural light from large windows, clean lines, beige and gray color palette, architectural digest style, ultra detailed, photorealistic",
        "negative": "anime, cartoon, illustration, painting, cluttered, dark, gothic, ornate, low quality, blurry",
        "params": {"steps": "25-35", "cfg": "3-4", "sampler": "dpmpp_2m", "guidance": "2.5-3.5"}
    },
    "flux_product_render": {
        "name": "FLUX 产品渲染",
        "category": "FLUX/写实",
        "positive": "professional product photography, white background, studio lighting setup, product hero shot, soft shadows, clean reflection on surface, commercial product photography style, high key lighting, 8k resolution, hyperrealistic, product visualization",
        "negative": "anime, cartoon, illustration, painting, messy background, harsh shadows, low quality, watermark, text",
        "params": {"steps": "20-30", "cfg": "3-4", "sampler": "euler", "guidance": "2-3"}
    },
    "flux_wildlife_photo": {
        "name": "FLUX 野生动物",
        "category": "FLUX/写实",
        "positive": "wildlife photography, African safari, golden hour lighting, shallow depth of field, sharp focus on animal eyes, natural habitat, dramatic sky, National Geographic style, Canon 1DX with 600mm lens, ultra detailed feathers or fur texture, behavioral wildlife moment, hyperrealistic",
        "negative": "anime, cartoon, illustration, painting, captive zoo setting, unnatural pose, blurry, low quality, domestic animal",
        "params": {"steps": "28-38", "cfg": "3.5-5", "sampler": "dpmpp_2m", "guidance": "3-4"}
    },
    "flux_street_night_china": {
        "name": "FLUX 中国夜景街拍",
        "category": "FLUX/写实",
        "positive": "night street photography in traditional Chinese city, red lanterns, neon signs reflecting on wet pavement, street food vendors, crowds of people, Shanghai or Chengdu alleyways, cinematic atmosphere, rich colors, street photography style, hyperrealistic, ultra detailed",
        "negative": "anime, cartoon, illustration, painting, daytime, sunny, empty streets, low quality, blurry",
        "params": {"steps": "28-35", "cfg": "3.5-5", "sampler": "euler_ancestral", "guidance": "3-4"}
    },

    # ========== FLUX 电影感 ==========
    "flux_cinematic_portrait": {
        "name": "FLUX 电影感人像",
        "category": "FLUX/电影感",
        "positive": "cinematic portrait, anamorphic lens flare, shallow depth of field, dramatic side lighting, film grain, Ridley Scott aesthetic, desaturated colors, moody atmosphere, 2.39:1 aspect ratio, 8k resolution, movie still quality, strong jawline, mysterious gaze",
        "negative": "anime, cartoon, illustration, painting, flat lighting, oversaturated, modern smartphone look, low quality, blurry",
        "params": {"steps": "30-40", "cfg": "3.5-5", "sampler": "dpmpp_2m", "guidance": "3-4", "resolution": "1792x768"}
    },
    "flux_mountain_epic": {
        "name": "FLUX 史诗山景",
        "category": "FLUX/电影感",
        "positive": "epic mountain landscape, dramatic clouds, golden hour sunlight breaking through storm clouds, vast vista, Himalayas or Zhangjiajie style, fog flowing through peaks, Ansel Adams photography style, 4x5 large format camera feel, ultra detailed, 8k resolution, cinematic color grading, 16:9 aspect ratio",
        "negative": "anime, cartoon, illustration, painting, simple, flat, low detail, blurry, daytime flat sky, oversaturated",
        "params": {"steps": "30-40", "cfg": "3.5-5", "sampler": "dpmpp_2m", "guidance": "3-4", "resolution": "1792x768"}
    },
    "flux_wuxia_hero": {
        "name": "FLUX 武侠英雄",
        "category": "FLUX/电影感",
        "positive": "wuxia martial arts hero standing on mountain peak, flowing traditional Chinese robes in wind, sword in hand, dramatic sunset, clouds below peak, Crouching Tiger Hidden Dragon aesthetic, cinematic composition, epic scale, ultra detailed traditional Chinese costume, atmospheric fog, 宽荧幕比例, movie quality",
        "negative": "anime, cartoon, illustration, painting, modern clothing, simple background, low quality, blurry, flat lighting",
        "params": {"steps": "30-40", "cfg": "3.5-5", "sampler": "dpmpp_2m", "guidance": "3-4", "resolution": "1792x768"}
    },
    "flux_interstellar_ship": {
        "name": "FLUX 星际飞船",
        "category": "FLUX/电影感",
        "positive": "massive spaceship emerging from hyperspace, blue-white engine glow, against backdrop of distant galaxy and nebula, Interstellar movie aesthetic, cinematic lighting, volumetric engine trails, ultra detailed ship exterior, 8k resolution, science fiction concept art quality, dramatic space opera composition",
        "negative": "anime, cartoon, illustration, painting, small scale, simple, low detail, blurry, toy-like ship design",
        "params": {"steps": "35-45", "cfg": "3.5-5", "sampler": "dpmpp_2m", "guidance": "3.5-5", "resolution": "1792x768"}
    },

    # ========== FLUX 插画/概念 ==========
    "flux_chinese_goddess": {
        "name": "FLUX 古风仙女",
        "category": "FLUX/插画",
        "positive": "traditional Chinese goddess in ethereal long white robes, flowing silk fabric dynamics, delicate jade ornaments in hair, lotus and peony flowers, misty mountain background, moonlight, Ink wash painting aesthetic meets photorealistic, Zhang Daqian style fusion, serene celestial expression, ultra detailed traditional Chinese fantasy art, 8k resolution",
        "negative": "anime, cartoon, illustration style, western fantasy armor, low quality, blurry, deformed, bad anatomy, extra limbs",
        "params": {"steps": "28-38", "cfg": "3.5-5", "sampler": "dpmpp_2m", "guidance": "3-4"}
    },
    "flux_chinese_landscape": {
        "name": "FLUX 中国山水",
        "category": "FLUX/插画",
        "positive": "traditional Chinese landscape painting in Guo Xi style, towering peaks with swirling mist, waterfalls cascading into rivers, ancient pavilions on cliffs, cypress trees, ink wash aesthetic with photorealistic details, sunrise over mountains, serene and grand, ultra detailed brushwork texture, 8k resolution",
        "negative": "anime, cartoon, western landscape, modern buildings, low quality, blurry, oversaturated colors",
        "params": {"steps": "28-38", "cfg": "3.5-5", "sampler": "dpmpp_2m", "guidance": "3-4"}
    },
    "flux_dragon_knight": {
        "name": "FLUX 龙骑士",
        "category": "FLUX/插画",
        "positive": "epic fantasy dragon knight in full plate armor, massive dragon circling above, medieval European castle in background, dramatic sunset, banner with heraldic symbols, Greg Rutkowski fantasy art style, cinematic composition, ultra detailed armor textures, dramatic lighting, 8k resolution, concept art quality",
        "negative": "anime, cartoon, simple, low quality, blurry, deformed armor, cartoonish dragon",
        "params": {"steps": "30-40", "cfg": "3.5-5", "sampler": "dpmpp_2m", "guidance": "3-4"}
    },
    "flux_ink_landscape": {
        "name": "FLUX 水墨山水",
        "category": "FLUX/插画",
        "positive": "contemporary Chinese ink wash landscape, minimalist composition, bamboo forest path, mountain silhouette in distance, misty atmosphere, sumi-e brushwork texture, black and white with subtle gray tones, traditional Chinese art aesthetic, serene temple in valley, ultra detailed ink simulation, 8k resolution",
        "negative": "anime, cartoon, colorful, oversaturated, western art style, low quality, blurry, digital looking",
        "params": {"steps": "25-35", "cfg": "3-4", "sampler": "euler", "guidance": "2.5-3.5"}
    },
    "flux_mech_warrior": {
        "name": "FLUX 机甲战士",
        "category": "FLUX/概念",
        "positive": "giant bipedal combat mech in futuristic battlefield, highly detailed mechanical design, panel lines and vents, glowing reactor core, weapon systems deployed, desert warzone, dust particles in air, Mecha anime aesthetic meets photorealistic, Gundam style, cinematic composition, 8k resolution, concept art quality",
        "negative": "anime, cartoon, chibi, simple robot, low quality, blurry, toy-like, flat colors",
        "params": {"steps": "30-40", "cfg": "3.5-5", "sampler": "dpmpp_2m", "guidance": "3-4"}
    },
    "flux_architecture_future": {
        "name": "FLUX 未来建筑",
        "category": "FLUX/概念",
        "positive": "futuristic sustainable architecture, bio-curved buildings covered in vertical gardens, solar glass panels, flying vehicles in sky, utopian cityscape, Singapore or Dubai inspired, Santiago Calatrava meets Zaha Hadid design language, hyperrealistic rendering, ultra detailed facade, 8k resolution, architectural visualization quality",
        "negative": "anime, cartoon, old architecture, run-down buildings, low quality, blurry, distorted perspective",
        "params": {"steps": "28-38", "cfg": "3-4", "sampler": "dpmpp_2m", "guidance": "3-4"}
    },
    "flux_underwater_world": {
        "name": "FLUX 水下世界",
        "category": "FLUX/概念",
        "positive": "underwater ancient city ruins, beams of light piercing through water surface, coral growing on architecture, exotic fish swimming, mystical atmosphere, Atlantis discovery moment, National Geographic underwater photography quality, volumetric light rays, blue-green color palette, hyperrealistic, 8k resolution",
        "negative": "anime, cartoon, above water, simple, low quality, blurry, dead coral, murky water",
        "params": {"steps": "28-38", "cfg": "3.5-5", "sampler": "dpmpp_2m", "guidance": "3-4"}
    },
    "flux_warriors_charge": {
        "name": "FLUX 将军冲锋",
        "category": "FLUX/概念",
        "positive": "ancient Chinese general on warhorse leading cavalry charge, battlefield smoke and dust, falling leaves, dramatic sky, Save I as a general Zhang Qian style, epic scale battle scene, traditional Han dynasty armor, ultra detailed battlefield debris, cinematic composition, 8k resolution, concept art quality",
        "negative": "anime, cartoon, modern clothing, peaceful scene, low quality, blurry, simple background",
        "params": {"steps": "30-42", "cfg": "3.5-5.5", "sampler": "dpmpp_2m", "guidance": "3.5-5"}
    },

    # ========== MJ 精选 ==========
    "mj_chinese_goddess": {
        "name": "MJ 古风美女",
        "category": "MJ/插画",
        "positive": "a beautiful Chinese woman in traditional Hanfu, delicate features, long flowing black hair with jade hairpin, standing in a misty bamboo forest, soft natural lighting, ethereal and serene atmosphere, traditional Chinese painting aesthetic, hyperrealistic portrait, 8k resolution, cinematic composition",
        "negative": "anime, cartoon, western features, deformed, bad anatomy, extra limbs, low quality",
        "params": {"steps": "25-35", "cfg": "7-8", "sampler": "DPM++ 2M Karras"}
    },
    "mj_fantasy_dragon": {
        "name": "MJ 奇幻龙",
        "category": "MJ/插画",
        "positive": "majestic dragon soaring through clouds above Chinese palace, golden scales shimmering, long whiskers flowing, imperial Chinese aesthetic, dramatic sunset clouds, intricate details on scales and whiskers, fantasy art, Voliyas style, ultra detailed, 8k resolution, epic composition",
        "negative": "cartoon, simple, low quality, blurry, deformed dragon, western dragon design",
        "params": {"steps": "30-40", "cfg": "7-8", "sampler": "DPM++ 2M Karras"}
    },
    "mj_emotional_portrait": {
        "name": "MJ 情感人像",
        "category": "MJ/摄影",
        "positive": "emotional portrait photography, soft Rembrandt lighting, contemplative gaze, shallow depth of field, film grain aesthetic, cinematic color grading, moody atmosphere, Annie Leibovitz style, black and white option, hyperrealistic, 8k resolution",
        "negative": "anime, cartoon, illustration, oversaturated, flat lighting, low quality, blurry",
        "params": {"steps": "25-35", "cfg": "7-8", "sampler": "DPM++ 2M Karras"}
    },
    "mj_vintage_camera": {
        "name": "MJ 复古相机",
        "category": "MJ/摄影",
        "positive": "vintage film camera on wooden table, warm tungsten light, film roll beside it, shallow depth of field, nostalgic mood, Kodak Portra film aesthetic, natural shadows, vintage photography workshop atmosphere, ultra detailed camera texture, 8k resolution, still life photography",
        "negative": "anime, cartoon, digital camera, modern, low quality, blurry, smartphone photo look",
        "params": {"steps": "25-35", "cfg": "7-8", "sampler": "DPM++ 2M Karras"}
    },

    # ========== 自然语言类 ==========
    "nl_brand_story": {
        "name": "自然语言 品牌故事",
        "category": "自然语言/创意",
        "positive": "brand story visual: a designer in their creative studio, morning light through large windows, wearing brand's latest collection, holding coffee, relaxed confident pose, minimalist industrial interior with plants, Morandi color palette, lifestyle brand aesthetic, magazine editorial quality",
        "negative": "over-edited, plastic feel, kitsch, low quality, blurry, amateurish, cartoon style",
        "params": {"steps": "30-38", "cfg": "3.5-5", "sampler": "dpmpp_2m_sde"}
    },
    "nl_profile_avatar": {
        "name": "自然语言 头像设计",
        "category": "自然语言/创意",
        "positive": "professional LinkedIn profile avatar, friendly approachable smile, modern professional attire, clean background with subtle gradient, natural headshot style, soft even lighting, confident but approachable expression, corporate professional quality, high resolution, suitable for business networking",
        "negative": "anime, cartoon, casual wear, cluttered background, harsh shadows, low quality, blurry, unprofessional",
        "params": {"steps": "20-28", "cfg": "3-4", "sampler": "euler"}
    },
    "nl_children_book": {
        "name": "自然语言 儿童绘本",
        "category": "自然语言/创意",
        "positive": "children's book illustration, a curious little fox exploring a magical forest at dusk, watercolor and digital hybrid style, warm golden hour light filtering through trees, mushrooms and fireflies, storybook aesthetic, gentle and magical atmosphere, suitable for children's ages 3-6, ultra detailed background elements",
        "negative": "scary, dark themes, realistic photographic style, violent content, low quality, blurry, adult themes",
        "params": {"steps": "25-35", "cfg": "3.5-5", "sampler": "dpmpp_2m"}
    },
    "nl_product_showcase": {
        "name": "自然语言 产品展示",
        "category": "自然语言/技术",
        "positive": "product showcase: minimalist product photography setup, product floating in center frame, soft shadows on infinite white curve, clean reflect on glass surface, key light and fill light setup visible, professional e-commerce product shot, hyperdetailed product texture, 8k resolution",
        "negative": "cluttered background, harsh shadows, low quality, blurry, amateurish product photo, watermark visible",
        "params": {"steps": "20-28", "cfg": "3-4", "sampler": "euler"}
    },
    "nl_tech_infographic": {
        "name": "自然语言 科技信息图",
        "category": "自然语言/技术",
        "positive": "tech infographic visual: abstract visualization of AI neural network, floating geometric nodes and connections, deep blue and cyan color scheme, dark background with glowing connections, holographic data visualization aesthetic, futuristic technology concept, ultra detailed, 8k resolution",
        "negative": "anime, cartoon, messy, low quality, blurry, outdated technology aesthetic, oversaturated",
        "params": {"steps": "25-35", "cfg": "3.5-5", "sampler": "dpmpp_2m"}
    },
    "nl_video_thumbnail": {
        "name": "自然语言 视频缩略图",
        "category": "自然语言/技术",
        "positive": "YouTube video thumbnail: dramatic before/after split composition, left side shows problem, right side shows solution, bold text area reserved at top, high contrast colors, emotionally engaging expression, ultra detailed, click-worthy thumbnail aesthetic, professional YouTube creator style",
        "negative": "boring composition, low contrast, small text area, blurry, low quality, amateurish thumbnail design",
        "params": {"steps": "20-28", "cfg": "3-4", "sampler": "euler"}
    },
}


# 获取所有预设名称（用于UI下拉菜单）
def get_preset_names():
    """返回所有预设的显示名称列表"""
    return [preset["name"] for preset in PRESETS.values()]


def get_preset_by_name(name):
    """根据名称查找预设"""
    for preset in PRESETS.values():
        if preset["name"] == name:
            return preset
    return None


def get_presets_by_category():
    """按类别分组返回所有预设"""
    categories = {}
    for key, preset in PRESETS.items():
        cat = preset["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((key, preset["name"]))
    return categories


# ComfyUI 节点类定义
NODE_CLASS = "PromptVaultLoader"

CATEGORY = "Prompt Vault/提示词库"

# 生成INPUT_TYPES的choices
PRESET_CHOICES = list(PRESETS.keys())

NODE_DISPLAY_NAME_MAP = {
    "PromptVaultLoader": "Prompt Vault 提示词选择器",
}


class PromptVaultLoader:
    """ComfyUI 自定义节点：从预设提示词库加载提示词"""

    CATEGORY = CATEGORY
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt", "parameters")
    FUNCTION = "load_preset"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        """定义节点的输入参数"""
        # 按类别组织预设，生成下拉菜单
        preset_options = []
        categories = get_presets_by_category()
        for cat, presets in sorted(categories.items()):
            for key, name in presets:
                preset_options.append(name)

        return {
            "required": {
                "preset": (preset_options, {
                    "default": "FLUX 人像大师",
                    "label": "选择预设提示词",
                    "description": "从提示词库中选择预设"
                }),
            }
        }

    def load_preset(self, preset):
        """加载选定的预设提示词"""
        found_preset = get_preset_by_name(preset)

        if not found_preset:
            # fallback
            found_preset = PRESETS["flux_portrait_master"]

        positive = found_preset["positive"]
        negative = found_preset["negative"]
        params = found_preset["params"]

        # 格式化参数字符串
        params_str = ", ".join([f"{k}: {v}" for k, v in params.items()])

        return (positive, negative, params_str)


# 导出节点类
__all__ = ["PromptVaultLoader"]

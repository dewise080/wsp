from modeltranslation.translator import TranslationOptions, register
from .models import websiteSetting, SeoSetting, headerFooterSetting


@register(websiteSetting)
class WebsiteSettingTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "author",
        "currency_name",
        "currency_symbol",
        "price_ragne",
        "address",
        "city",
        "country",
        "state",
    )


@register(SeoSetting)
class SeoSettingTranslationOptions(TranslationOptions):
    fields = (
        "meta_title",
        "tag_line",
        "meta_description",
        "seo_keywords",
    )


@register(headerFooterSetting)
class HeaderFooterSettingTranslationOptions(TranslationOptions):
    fields = (
        "header_button_text",
        "header_button_url",
        "footer_col1_description",
        "footer_copyright",
    )

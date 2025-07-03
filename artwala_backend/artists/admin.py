from django.contrib import admin
from .models import ArtistProfile, ArtistReview

@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'user', 'slug', 'commission_available', 'featured', 'rating', 'created_at')
    list_filter = ('commission_available', 'featured', 'created_at')
    search_fields = ('display_name', 'user__email', 'user__username')
    prepopulated_fields = {'slug': ('display_name',)}
    readonly_fields = ('rating', 'total_reviews', 'created_at', 'updated_at')

@admin.register(ArtistReview)
class ArtistReviewAdmin(admin.ModelAdmin):
    list_display = ('artist', 'reviewer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('artist__display_name', 'reviewer__email')

def force_image_loading(page):
    """Force eager loading of all images for consistent visual testing"""
    page.evaluate(
        """() => {
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            // Force immediate load
            img.loading = 'eager';
            // Create a new Image object to trigger load
            const preloader = new Image();
            preloader.src = img.src;
        });
    }"""
    )

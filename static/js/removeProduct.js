function removeProduct(productId) {
    fetch(`/cart/remove/${productId}`, {
        method: 'GET'
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    }).catch(error => {
        console.error('Error removing product:', error);
    });
}
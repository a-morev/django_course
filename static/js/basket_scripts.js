'use strict';

window.onload = function () {
    console.log('DOM ready');
    let basketList = $('.basket_list');
    // ловим событие "изменить" на селекторе input
    basketList.on('change', 'input[type=number].product_quantity', function (event) {
        $.ajax({
            url: '/basket/change/' + event.target.name + '/quantity/' + event.target.value + '/',
            success: function (data) {
                basketList.html(data.basket_items);
            },
        });
    })
}

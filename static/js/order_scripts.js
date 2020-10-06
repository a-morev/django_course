"use strict";

let _quantity, _price, orderitemNum, deltaQuantity, orderitemQuantity, deltaCost;
let quantityArr = [];
let priceArr = [];
let $orderTotalQuantityDOM;

let totalForms;
let orderTotalQuantity;
let orderTotalCost;
let $orderForm;


function parseOrderForm() {
    for (let i = 0; i < totalForms; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantityArr[i] = _quantity;
        priceArr[i] = (_price) ? _price : 0;
    }
}

function orderSummaryUpdate(orderitemPrice, deltaQuantity) {
    deltaCost = orderitemPrice * deltaQuantity;
    orderTotalCost = Number((orderTotalCost + deltaCost).toFixed(2));
    orderTotalQuantity = orderTotalQuantity + deltaQuantity;

    $('.order_total_cost').html(orderTotalCost.toString());
    $orderTotalQuantityDOM.html(orderTotalQuantity.toString());
}

function deleteOrderItem(row) {
    let targetName = row[0].querySelector('input[type="number"]').name;
    orderitemNum = parseInt(targetName.replace('orderitems-', '').replace('-quantity', ''));
    deltaQuantity = -quantityArr[orderitemNum];
    quantityArr[orderitemNum] = 0;
    if (!isNaN(priceArr[orderitemNum]) && !isNaN(deltaQuantity)) {
        orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
    }
}

function updateTotalQuantity() {
    for (let i = 0; i < totalForms; i++) {
        orderTotalQuantity += quantityArr[i];
        orderTotalCost += quantityArr[i] * priceArr[i];
    }
    $orderTotalQuantityDOM.html(orderTotalQuantity.toString());
    $('.order_total_cost').html(Number(orderTotalCost.toFixed(2)).toString());
}

function orderSummaryRecalc() {
    orderTotalQuantity = 0;
    orderTotalCost = 0;

    for (let i = 0; i < totalForms; i++) {
        orderTotalQuantity += quantityArr[i];
        orderTotalCost += quantityArr[i] * priceArr[i];
    }
    $orderTotalQuantityDOM.html(orderTotalQuantity.toString());
    $('.order_total_cost').html(Number(orderTotalCost.toFixed(2)).toString());
}

window.onload = function () {
    $orderTotalQuantityDOM = $('.order_total_quantity');
    totalForms = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    orderTotalQuantity = parseInt($orderTotalQuantityDOM.text()) || 0;
    orderTotalCost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;
    $orderForm = $('.order_form');

    parseOrderForm();

    if (!orderTotalQuantity) {
        updateTotalQuantity();
    }

    $orderForm.on('change', 'input[type="number"]', function (event) {
        orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace(
            '-quantity', ''));
        if (priceArr[orderitemNum]) {
            orderitemQuantity = parseInt(event.target.value);
            deltaQuantity = orderitemQuantity - quantityArr[orderitemNum];
            quantityArr[orderitemNum] = orderitemQuantity;
            orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
        }
    });

    $orderForm.on('change', 'input[type="checkbox"]', function (event) {
        orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (event.target.checked) {
            deltaQuantity = -quantityArr[orderitemNum];
        } else {
            deltaQuantity = quantityArr[orderitemNum];
        }
        orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
    });

    $('.formset_row').formset({
        addText: 'выбрать еще колбаски',
        deleteText: 'убрать',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    $('.order_form select').change(function (event) {
        let target = event.target;
        let orderitemNum = parseInt(target.name.replace('orderitems-', '').replace(
            '-product', ''));
        let orderitemProductPk = target.options[target.selectedIndex].value;

        if (orderitemProductPk) {
            $.ajax({
                url: "/product/" + orderitemProductPk + "/price/",
                success: function (data) {
                    // console.log('get product price', data);
                    if (data.price) {
                        priceArr[orderitemNum] = parseFloat(data.price);
                        if (isNaN(quantityArr[orderitemNum])) {
                            quantityArr[orderitemNum] = 0;
                        }
                        let priceHtml = '<span>' +
                            data.price.toString().replace('.', ',') +
                            '</span> &#8381;';
                        let currentTr = $('.order_form table').find('tr:eq(' + (orderitemNum + 1) + ')');

                        currentTr.find('td:eq(2)').html(priceHtml);

                        if (isNaN(currentTr.find('input[type="number"]').val())) {
                            currentTr.find('input[type="number"]').val(0);
                        }
                        orderSummaryRecalc();
                    }
                },
            });
        }
    });
};
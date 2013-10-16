$(function(){
    if (!window['eventMapParams']) {
        return;
    }

    ymaps.ready(function(){
        var myMap = new ymaps.Map("map", {
            center: eventMapParams.coords,
            zoom: 15
        }),
        myPlacemark = new ymaps.Placemark(eventMapParams.coords, {
            balloonContent: eventMapParams.baloonContent
        });
        myMap.geoObjects.add(myPlacemark);
        myMap.controls.add('smallZoomControl');

        $('.event__map-placeholder').on('click', function(){
            $(this).remove();
        });
    });
});

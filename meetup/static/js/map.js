$(function(){
    ymaps.ready(function(){
        var myMap = new ymaps.Map("map", {
            center: event.coords,
            zoom: 15
        }),
        myPlacemark = new ymaps.Placemark(event.coords, {
            balloonContent: event.baloonContent
        });
        myMap.geoObjects.add(myPlacemark);
        myMap.controls.add('smallZoomControl');

        $('.event__map-placeholder').on('click', function(){
            $(this).remove();
        });
    });
});

$(function() {
    // Cache selectors
    var lastId;
    var topMenu = $("header nav");
    var topMenuHeight = topMenu.parents(".container").outerHeight();
    // All list
    var menuItems = topMenu.find("a");
    // Anchors corresponding to menu items
    var scrollItems = menuItems.map(function(){
        if ($(this).attr("href").indexOf("#") == 0) {
            var item = $($(this).attr("href"));
            if (item.length) { return item; }
        }
    });
    if (location.hash) {
        var href = location.hash;
        var offsetTop = href === "#" ? 0 : $(href).offset().top-topMenuHeight+1;
        $('html, body').stop().animate({
           scrollTop: offsetTop+15
        }, 300);
    }

    // Bind click handler to menu items
    // so we can get a fancy scroll animation
    menuItems.click(function(e){
        var href = $(this).attr("href");
        if ($(this).attr("href").indexOf("#") != 0) {
            return true;
        }
        var offsetTop = href === "#" ? 0 : $(href).offset().top-topMenuHeight+1;
        $('html, body').stop().animate({
            scrollTop: offsetTop+15
        }, 300);
        e.preventDefault();
    });

    // Bind to scroll
    $(window).scroll(function(){
        // Get container scroll position
        var fromTop = $(this).scrollTop()+topMenuHeight;

        // Get id of current scroll item
        var cur = scrollItems.map(function(){
            if ($(this).offset().top < fromTop)
                return this;
        });
        // Get the id of the current element
        cur = cur[cur.length-1];
        var id = cur && cur.length ? cur[0].id : "";

        if (lastId !== id) {
            lastId = id;
            // Set/remove active class
            $(menuItems).removeClass("active").filter("[href=#"+id+"]").addClass("active");
        }
    });

});

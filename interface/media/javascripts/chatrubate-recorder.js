const popup = function(url='/wishlist/add', width=500, height=500) 
{
    this.width = width;
    this.height = height;
    this.url = url;
    
    this.blocker = jQuery('<div id="popup-blocker"></div>').on( "click", this.hide.bind(this));
    this.popup = jQuery('<div id="popup"></div>');
    
    jQuery( window ).resize(this.resize.bind(this));
    this.show(url);
    this.resize()
}
popup.prototype.hide = function()
{
    jQuery(this.blocker).remove();
    jQuery(this.popup).remove();
}
popup.prototype.show = function(url)
{
    jQuery('body').append(this.blocker);
    jQuery('body').append(this.popup);
    
    jQuery.ajax(
        {
            url: url,
        }
    ).done(
        function(data)
        {
            jQuery(this.popup).html(data);
        }.bind(this)
    );
}

popup.prototype.resize = function()
{
    const windowWidth = $( window ).width();
    const windowHeight = $( window ).height();
    
    
    const leftPos = parseInt((windowWidth - this.width) / 2);
    const topPos = parseInt((windowHeight - this.height) / 2);
    
    jQuery(this.popup).css(
        {
            'left': leftPos,
            'top': topPos,
            'width': this.width,
            'height': this.height,
            
        }
    );
}

const recorder = function(toolbar = false, wishlist = false, videolist = false) {
    
    this.toolbar = toolbar;
    this.wishlist = wishlist;
    this.videolist = videolist;
    
    this.toolbarOptions = {
        '+': this.addWish
    };
    
    this.renderToolbar();
    jQuery(this).on( "wishlist:change", this.refreshWishlist.bind(this));
    this.refreshWishlist();
    
    this.heartbeat = setInterval(this.refrashAll.bind(this), 5000);
}
recorder.prototype.refrashAll = function() {
    jQuery(this).trigger( "wishlist:change" );
}
recorder.prototype.addWish = function() {
    new popup('/wishlist/add');
}
recorder.prototype.renderToolbar = function() {
    
    if(!this.toolbar)
    {
        return false;
    }
    
    
    for (var option in this.toolbarOptions) 
    {
        const button = jQuery(
          '<button>'
        ).attr(
          'class', 
          option
        ).text(
          option
        ).click( 
          this.toolbarOptions[option].bind(this) 
        );

        jQuery(this.toolbar).append(button);
    }
}
recorder.prototype.refreshWishlist = function() {
    if(!this.wishlist)
    {
        return false;
    }
    
    $.ajax(
        {
            url: "/wishlist",
        }
    ).done(
        this.renderWishlist.bind(this)
    );
}
recorder.prototype.renderWishlist = function(data) 
{
    if(!this.wishlist)
    {
        return false;
    }
    
    jQuery(this.wishlist).html('');
    
    
    for (var item in data) 
    {
        const itemObj = jQuery(
          '<li class="recording-' + data[ item ].status + '">'
        ).html(
          '<span>' + data[ item ].title + ' <a href="/wishlist/delete/' + data[ item ].id + '/">delete</a></span>'
        )

        jQuery(this.wishlist).append(itemObj);
    }
}

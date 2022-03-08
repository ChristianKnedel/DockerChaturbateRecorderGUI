const popup = function(url='/wishlist/add', width=500, height=500) 
{
    this.width = width;
    this.height = height;
    this.url = url;
    
    this.blocker = jQuery('<div id="popup-blocker"></div>');
    this.popup = jQuery('<div id="popup"></div>');
    
    jQuery( window ).resize(this.resize.bind(this));
}
popup.prototype.show = function()
{
    jQuery('body').append(this.blocker);
    jQuery('body').append(this.popup);
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
            'top': topPos
        }
    );
}

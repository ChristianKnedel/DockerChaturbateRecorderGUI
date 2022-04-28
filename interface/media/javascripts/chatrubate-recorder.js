const popup = function(url='/wishlist/add', width=500, height=500, title='NEW ITEM') 
{
    this.width = width;
    this.height = height;
    this.url = url;
    
    this.blocker = jQuery('<div id="popup-blocker"></div>').on( "click", this.hide.bind(this));
    this.popup = jQuery('<div id="popup"><h1>' + title + '<span>X</span></h1><div class="inner"></div></div>');
    
    jQuery( window ).resize(this.resize.bind(this));
    jQuery( this.popup ).find('h1 span').click(this.hide.bind(this));
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
            jQuery(this.popup).find('div.inner').html(data);
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
        '+': this.addWish,
        'Dark/Light Mode': this.toggleDarkMode
    };
    
    this.renderToolbar();
    jQuery(this).on( "wishlist:change", this.refreshWishlist.bind(this));
    this.refreshWishlist();
    
    $("body").attr('class', this.loadSetting('color-mode'))
    
    this.heartbeat = setInterval(this.refrashAll.bind(this), 5000);
}
recorder.prototype.loadSetting = function(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
recorder.prototype.saveSetting = function(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
recorder.prototype.toggleDarkMode = function() {
    $("body").toggleClass("dark", "");
    this.saveSetting('color-mode', $("body").attr('class'), 100000);
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
        let icon = '<i class="fa fa-video"></i>';
        
        if(data[ item ].type === 'f')
        {
           icon = '<i class="fa fa-search"></i>';
        }
        
        const itemObj = jQuery(
          '<li class="type-' + data[ item ].type  + '-recording-' + data[ item ].status + '">'
        ).html(
          '<span>' + icon + '&nbsp;&nbsp;&nbsp;' + data[ item ].gender + ' / ' + data[ item ].title + ' <a href="/wishlist/delete/' + data[ item ].id + '/"><i class="fa-solid fa-trash"></i></a></span>'
        )

        jQuery(this.wishlist).append(itemObj);
    }
}

$(document).ready ->
    #Map Jquery
    map = new GMaps(
      el: '#map'
      scrollwheel: false
      lat: 34.7667
      lng: 32.4167
      zoom: 14
      zoomControl: true
      zoomControlOpt:
        style: 'SMALL'
        position: 'TOP_LEFT'
      panControl: false
      streetViewControl: false
      mapTypeControl: false
      overviewMapControl: false)
    map.addMarker
      lat: 34.7667
      lng: 32.4167
      icon: '/static/images/map-marker.png'
    styles = [
      {
        featureType: 'road'
        elementType: 'geometry'
        stylers: [
          { lightness: 100 }
          { visibility: 'simplified' }
        ]
      }
      {
        featureType: 'road'
        elementType: 'labels'
        stylers: [ { visibility: 'off' } ]
      }
    ]
    map.addStyle
      styledMapName: 'Styled Map'
      styles: styles
      mapTypeId: 'map_style'
    map.setStyle 'map_style'
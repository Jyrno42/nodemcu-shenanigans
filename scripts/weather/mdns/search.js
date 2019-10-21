const mdns = require('multicast-dns')();

mdns.on('response', function (response) {
    console.log('got a response packet:', response);
    mdns.destroy();
});

mdns.query({
    questions:[{
      name: 'dashboard.plants.local',
      type: 'A'
    }]
});


const os = require('os');

const mdns = require('multicast-dns')();

let localIp = null;

Object.values(os.networkInterfaces()).forEach((interface) => {
    interface.forEach((info) => {
        if (info.internal) {
            return;
        }

        if (info.family !== 'IPv4') {
            return;
        }

        localIp = info.address;
    });
});

console.warn('Advertising `dashboard.plants.local` A', localIp);

mdns.on('response', function (response) {
    console.log('got a response packet:', response);
})

mdns.on('query', function (query) {
    const answers = [];

    for (const question of query.questions) {
        switch (question.name) {
            // All the hosts we want to advertise
            case 'dashboard.plants.local':
                answers.push({
                    name: question.name,
                    type: 'A',
                    ttl: 300,
                    data: localIp
                });

            default:
                break;
        }
    }

    if (answers.length > 0) {
        mdns.respond({ answers });
    }
});

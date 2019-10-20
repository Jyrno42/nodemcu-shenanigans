const mdns = require('multicast-dns')();

mdns.on('response', function (response) {
    console.log('got a response packet:', response);
})

mdns.on('query', function (query) {
    const answers = [];

    for (const question of query.questions) {
        switch (question.name) {
            // All the hosts we want to advertise
            case 'plants-controller.local':
                answers.push({
                    name: question.name,
                    type: 'A',
                    ttl: 300,
                    data: '192.168.1.5' // TODO: Get actual IP of current machine
                });

            default:
                break;
        }
    }

    if (answers.length > 0) {
        mdns.respond({ answers });
    }
});

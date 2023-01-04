const mqtt = require('mqtt')
const rest = require('restler')
const event_key = "your key on webook documentation"
const url = 'mqtt://your IP address'


exports.handler = function(context, event) {

    var out = parseInt(event.body);

    if(out == 1){
        rest
            .post(
                "https://maker.ifttt.com/trigger/alarm_detector/with/key/" +
                event_key, {
                    data: {
                        value1: "ALARM TRIGGERED"
                    },
                }
            )
            .on("complete", function(data) {
                console.log(
                    "Allarme Inviato"
                );
            });
    }
    context.callback("");
};
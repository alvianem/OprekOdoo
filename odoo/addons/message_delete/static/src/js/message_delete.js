odoo.define('message_delete.message_delete', function (require) {
"use strict";

var core = require('web.core');
var data = require('web.data');
var _t = core._t;
var chat_manager = require('mail.chat_manager');
var ChatThread = require('mail.ChatThread');


function get_channel_cache (channel, domain) {
    var stringified_domain = JSON.stringify(domain || []);
    if (!channel.cache[stringified_domain]) {
        channel.cache[stringified_domain] = {
            all_history_loaded: false,
            loaded: false,
            messages: [],
        };
    }
    return channel.cache[stringified_domain];
}

// Function for cache clearing
function remove_message_from_channel (channels, channel_id, message) {
    var channel = _.findWhere(channels, { id: channel_id });
    _.each(channel.cache, function (cache) {
        cache.messages = _.without(cache.messages, message);
    });
}

ChatThread.include({

    init: function (parent, options) {
        this._super(parent, options);
        this.events = _.extend(this.events || {},{
            'click .fa-trash': 'on_message_deleting',
        })
    },

    on_message_deleting: function (event) {
        event.stopPropagation();
        var done = $.Deferred();
        if (! confirm(_t("Do you really want delete this message?"))) { return false; }
        var self = this;
        var message_id = event.target.dataset['messageId'],
            channel_id = parseInt(event.target.dataset['channelId'], 10),
            message = chat_manager.get_message(parseInt(message_id, 10)),
            parent = self.getParent();
        if (! channel_id) {
            channel_id = event.target.dataset['channelId'];
        }
        console.log("Message", message)
        var Message = new data.DataSetSearch(this, 'mail.message');
        Message.context.message_delete = 1;
        Message.call('unlink', [parseInt(message_id), Message.context]).then(function(answer){
            if (answer) {
                // Re-render page, if channel is defined. Otherwise, reload page
                if (channel_id) {
                    // Clearing cache to prevent race condition, where JS re-rendering page with deleted message
                    var chanel = chat_manager.get_channel(channel_id);
                    remove_message_from_channel([chanel], channel_id, message);
                    var chanel_cache = get_channel_cache(chanel, parent.domain),
                        messages = chanel_cache.messages,
                        options = parent.get_thread_rendering_options(messages);
                    // Deleting message from webview and rendering page
                    self.remove_message_and_render(message_id, messages, options);
                }
                else {
                    location.reload();
                }
            }
            else {
                return done;
            }
        });
        return done;
        }
    });
});

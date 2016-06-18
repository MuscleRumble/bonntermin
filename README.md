# bonntermin

Automatically scrape _Stadt Bonn's Dienstleistungszentrum_ appointment service for the earliest month that you can reserve. If this bookable month is the one you desire, you'll receive an email notification.

## Requirements

Python dependencies:

```sh
pip install scrapy dateparser
```

## Customization

There are two files that you have to customize in order to make full use of the scrape's result.

### spiders/bonn.py

You have to modify the variables `form_data`, `wanted_year`, `wanted_month`, `notification_email`.

The appropiate values for `form_data` can be found [here](https://netappoint.de/ot/stadtbonn/?company=stadtbonn). Just look into the source code of the website. The example `{'casetype_9664': '1', 'casetype_9656': '1'}` stands for _Personalausweis-Antrag_ and _Reisepass-Antrag_ respectively.

If the spider finds that the earliest bookable date is equal to your `wanted_month` and `wanted_year`, it will send an email to `notification_email`.

### settings.py

Add your SMTP server settings according to [Scrapy's documentation](http://doc.scrapy.org/en/latest/topics/email.html#topics-email-settings), otherwise you won't receive an email notification.

## Periodic Job

Obviously, for this to make sense you should set up a periodic job. You could do that locally on your machine, but you could also use a service like [Scrapinghub](http://scrapinghub.com/). This is highly recommended and [it's very easy to set up](http://doc.scrapinghub.com/shub.html).

## License

Distributed under the MIT license. See the LICENSE file for more info.

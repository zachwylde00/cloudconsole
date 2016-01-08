#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import config
from config import log
from crawler import aws
from storage import writer


def get_cmd_parser():
    parser = argparse.ArgumentParser(
            description='Cloud Config cli tool',
            epilog='Author ashokraja.r@gmail.com | Feedback most welcomed,'
                   'even better a pull request.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', action='version',
                        version='%(prog)s 1.0.dev1')

    parser.add_argument('runcrawler',
                        help='Starts to crawl your infrastructure.')

    return parser.parse_args()


def crawl_aws():
    log.info("AWS ec2 crawler started")
    for region in config.REGIONS:
        log.info("AWS ec2 crawler : crawling region=%s" % region)
        ec2 = aws.Ec2(region=region)
        ec2.crawl_all_instance()
    log.info("AWS ec2 crawler finished")

    log.info("AWS elb crawler started")
    for region in config.REGIONS:
        log.info("AWS elb crawler : crawling region=%s" % region)
        elb = aws.Elb(region=region)
        elb.crawl_all_elb()
    log.info("AWS elb crawler finished")


if __name__ == '__main__':
    args = get_cmd_parser()

    if args.runcrawler:
        writer.init_datastore()
        crawl_aws()
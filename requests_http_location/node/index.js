#!/usr/bin/env node

import axios from 'axios';
import got from 'got';

const fetch_response = await fetch(process.argv[2]);
console.log(fetch_response);

axios.get(process.argv[2])
  .then(function (response) {
    // handle success
    console.log(response);
  })

const got_response = await got(process.argv[2], {});
console.log(got_response)

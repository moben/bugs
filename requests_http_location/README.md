# What Is This?

A comparison of how different http clients handle redirects

Run example server

```
% python3 -m server 8080

valid_redirect_target=…
invalid_redirect_target=…

Request 'http://localhost:8080/v' or 'http://localhost:8080/i', following redirects

Press Enter when done to exit...
```

Test different clients agains either a correctly escaped redirect at `/v` or an invalid one at `/i`. (Set `USE_NIX=1` if `nix develop` is available but `go`, `cargo`, `npm`, `java` and common python http clients are not)

```
% python3 clients.py http://localhost:8080/v
```

View requested paths on the server side

```
…
Press Enter when done to exit...

<Enter>

The following paths were requested by these User-Agents:

  - /v, /v/%7E__-.~__0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%21%22%23%24%25%26%27%28%29%2A%2B%2C-./%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~%20%09%0A%0D%0B%0C__
    - Go-http-client/1.1
    - Java-http-client/21.0.5
    - Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
    - Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
    - Python-urllib/3.13
    - axios/1.8.4
    - curl/8.12.1
    - go-resty/3.0.0-beta.1 (https://resty.dev)
    - got (https://github.com/sindresorhus/got)
    - node
    - python-httpx/0.28.1
    - python-urllib3/2.3.0
    - requests-patched
    - reqwest

  - /v, /v/~__-.~__0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%21%22%23%24%25%26%27%28%29%2A%2B%2C-./%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~%20%09%0A%0D%0B%0C__
    - python-requests/2.32.3
```

# Results

As of 2025-03-28

## Valid Redirect

Redirect target:
```
/v/%7E__-.~__0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%21%22%23%24%25%26%27%28%29%2A%2B%2C-./%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~%20%09%0A%0D%0B%0C__
```

```
The following paths were requested by these User-Agents:

  - /v, /v/%7E__-.~__0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%21%22%23%24%25%26%27%28%29%2A%2B%2C-./%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~%20%09%0A%0D%0B%0C__
    - Go-http-client/1.1
    - Java-http-client/21.0.5
    - Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
    - Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
    - Python-urllib/3.13
    - axios/1.8.4
    - curl/8.12.1
    - go-resty/3.0.0-beta.1 (https://resty.dev)
    - got (https://github.com/sindresorhus/got)
    - node
    - python-httpx/0.28.1
    - python-urllib3/2.3.0
    - requests-patched
    - reqwest

  - /v, /v/~__-.~__0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%21%22%23%24%25%26%27%28%29%2A%2B%2C-./%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~%20%09%0A%0D%0B%0C__
    - python-requests/2.32.3
```

## Invalid Redirect

Redirect target:
```
/i/%^1%__%%/%7E__-.~__abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 !"$%&\'()*+,-./:;<=>?@[\\]^_`{|}~__
```

```
The following paths were requested by these User-Agents:

  - /i, /i/%^1%__%%/%7E__-.~__abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%200123456789%20!"$%&'()*+,-./:;<=>?@[\]^_`{|}~__
    - Python-urllib/3.13
    - curl/8.12.1

  - /i, /i/%%5E1%__%%/%7E__-.~__abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%200123456789%20!%22$%&'()*+,-./:;%3C=%3E?@[\]^_`{|}~__
    - Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
    - Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0

  - /i
    - Go-http-client/1.1
    - Java-http-client/21.0.5
    - go-resty/3.0.0-beta.1 (https://resty.dev)

  - /i, /i/%^1%__%%/%7E__-.~__abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%200123456789%20!%22$%&'()*+,-./:;%3C=%3E?@[\]^_`{|}~__
    - axios/1.8.4
    - got (https://github.com/sindresorhus/got)
    - node
    - python-httpx/0.28.1
    - reqwest

  - /i, /i/%25%5E1%25__%25%25/%257E__-.~__abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%200123456789%20!%22$%25&'()*+,-./:;%3C=%3E?@%5B%5C%5D%5E_%60%7B%7C%7D~__
    - python-urllib3/2.3.0
    - requests-patched

  - /i, /i/%25%255E1%25__%25%25/~__-.~__abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%25200123456789%2520!%2522$%25&'()*+,-./:;%253C=%253E?@%5B%5C%5D%5E_%60%7B%7C%7D~__
    - python-requests/2.32.3
```

# Interpretation

`python-requests` is the only user agent that re-quotes correctly escaped targets.  This has been observed to break some redirects on the public internet.

For invalid targets, behavior differs wildly. Options seem to be:

  - Don't follow invalid redirects, raise an error: stdlib of `java`, `go`
  - Quote some invalid characters:
    - spaces only: `curl`, `urllib`
    - spaces and invalid escape sequences (still yielding invalid escape sequences): `gecko`, `chromium`
    - all characters except reserved/unreserved, ignoring invalid escape sequences: `node`, `httpx`, `got`, `reqwest`
    - all except unreserved characters (double quoting valid escape sequences): `urllib3`
    - invalid escape sequences and characters except reserved/unreserved, unquoting unreserved. Then re-escaping/double-escapint the result through `urllib3`: `requests`

#!/usr/bin/env python3
import sys
import re

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as f:
    content = f.read()

# Adicionar meta tags de segurança após <title>
security_meta_tags = '''    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' fonts.googleapis.com; connect-src 'self';" />
    <meta http-equiv="X-Frame-Options" content="SAMEORIGIN" />
    <meta http-equiv="X-Content-Type-Options" content="nosniff" />
    <meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin" />
    <meta http-equiv="Permissions-Policy" content="geolocation=(), microphone=(), camera=(), payment=()" />
    <meta name="theme-color" content="#0F0F0F" />
    <meta name="description" content="InfiniteClaud - Plugin Oficial Claude com 50x aceleração, 96% menos tokens e 20+ ferramentas MCP nativas" />'''

# Inserir após a primeira tag meta (charset)
content = re.sub(
    r'(<meta charset="UTF-8" />)',
    r'\1\n' + security_meta_tags,
    content,
    count=1
)

with open(output_file, 'w') as f:
    f.write(content)

print(f"✅ Headers de segurança adicionados a {output_file}")

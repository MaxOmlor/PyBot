GLOBAL_DICT = {}

def trans(text):
    if not text:
        return text
    if '->' in text:
        var = None
        args, code = [p.strip() for p in text.split('->')]
        if '=' in args:
            var, args = [p.strip() for p in args.split('=')]
        if args[0] == '(' and args[-1] == ')':
            args = args[1:-1]
        if var:
            #return f'{var} = lambda {args}: {code}'
            return f'def {var}({args}): return {code}'
        return f'lambda {args}: {code}'
    return text

def get_response(code_py_bot_update):
    global GLOBAL_DICT
    code_py_bot_text = trans(code_py_bot_update.message.text)
    code_py_bot_reply_to_msg = code_py_bot_update.message.reply_to_message.text if code_py_bot_update.message.reply_to_message else None
    code_py_bot_reply_to_msg = trans(code_py_bot_reply_to_msg)
    print(f'{code_py_bot_text=}')

    exec(code_py_bot_text, GLOBAL_DICT)
    GLOBAL_DICT = {k:v for k,v in {**GLOBAL_DICT, **locals()}.items() if k not in globals() and 'code_py_bot' not in k}
    print(f'{GLOBAL_DICT=}')

    code_py_bot_response = None
    try:
        code_py_bot_response = eval(code_py_bot_text, GLOBAL_DICT)
        if code_py_bot_reply_to_msg:
            code_py_bot_response = code_py_bot_response(eval(code_py_bot_reply_to_msg))
    except:
        code_py_bot_response = None
    GLOBAL_DICT = {k:v for k,v in {**GLOBAL_DICT, **locals()}.items() if k not in globals() and 'code_py_bot' not in k}
    return code_py_bot_response




def handle_help(update, context):
    help_text = \
'''commands:
/namespace: returns all defined variables, functions, classes, etc. in this namespace
<text>: sended messages get interpreted as python code. result gets returned.
'''
    update.message.reply_text(help_text)

def handle_namespace(update, context):
    global GLOBAL_DICT
    print(f'{update.message.text=}')
    print(f'{GLOBAL_DICT=}')

    namespace_str = 'None' if len(GLOBAL_DICT) == 0 else '\n'.join([f'{k}: {v}' for k,v in GLOBAL_DICT.items()])

    #update.message.reply_text(GLOBAL_DICT)
    update.message.reply_text(namespace_str)

def handle_msg(update, context):
    response = get_response(update)
    response_str = str(response)

    update.message.reply_text(response_str)

def error(update, context):
    print(f'error caused by:\n{str(update)=}\n{str(context)=}')
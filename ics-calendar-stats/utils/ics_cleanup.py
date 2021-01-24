def cleanup_ics_string(ics_str: str):
    # Remoe the characters that mess with parsing
    clean_str = ics_str.replace(' ', '')

    res_lines = []
    in_description = False
    line_count = 0

    # Limit the size of DESCRIPTION to 15 lines
    line_limit = 15
    for line in clean_str.splitlines():
        if in_description and not line.startswith(' '):
            in_description = False
        if line.startswith('DESCRIPTION:'):
            in_description = True
            line_count = 0
        if in_description:
            if line_count == line_limit:
                res_lines.append(' ... Truncated ...')
            line_count += 1
            if line_count > line_limit:
                continue
        res_lines.append(line)
    return '\n'.join(res_lines)

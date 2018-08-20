import json
import sys

def special_chars(str):
    return str.replace('$', '\\$').replace('%', '\\%').replace('#', '\\#')

def comment(title):
    return '%---- ' + title + ' -----\n'

def format(title, tex):
    return comment(title) + special_chars(tex)

def skills(title, fname):
    tex = '\\section{' + title +'}\n' + '\\resumeSubHeadingListStart\n'
    with open(fname) as f:
        data = json.load(f)[title]
        for itemW in data:
            for item in itemW:
                tex += '\\resumeSubItem{' + item + '}\n'
                tex += '{' + itemW[item] + '}\n'
    return format(title, tex) + "\\resumeSubHeadingListEnd"

def experience(title, fname):
    tex = '\\section{' + title +'}\n' + '\\resumeSubHeadingListStart\n\n'
    with open(fname) as f:
        data = json.load(f)[title]
        for org in data:
            tex += '\\resumeSubheading\n'
            tex += '{' + org['organization'] + '}'
            tex += '{' + org['location'] + '}'
            tex += '{' + org['position'] + '}'
            tex += '{' + org['period'] + '}'
            tex += '\n\\resumeItemListStart\n'
            for bullet in org['description']:
                tex += '\\item {' + bullet + '}\n'
            tex += '\\resumeItemListEnd\n\n'
    return format(title, tex) + '\\resumeSubHeadingListEnd\n\n'

def education(title, fname):
    tex = '\\section{' + title + '}\n\\resumeSubHeadingListStart\n' + '\\resumeSubheading\n'
    with open(fname) as f:
        data = json.load(f)[title]
        for item in data:
            tex += '{' + data[item] + '}'
    return format(title, tex) + '\n\\resumeSubHeadingListEnd\n\n'

def info( title, fname):
    tex = '\\begin{tabular*}{\\textwidth}{l@{\extracolsep{\\fill}}r}\n'
    with open(fname) as f:
        data = json.load(f)['info']
        tex += '\\textbf{\href{' + data['personal_web'] + '}{\\Large ' + data['name'] + '}} & \\href{' + data['personal_web'] + '}{' + data['personal_web'] + '} \\\\'
        tex += '\n\\href{mailto:' + data['email'] + '}{' + data['email'] + '} & \href{' + data['github'] + '}{' + data['github'] + '} \\\\'
        tex += '\n' + data['phone'] + ' & \href{' + data['linkedin'] + '}{' + data['linkedin'] + '} \\\\\n'
    return format(title, tex) + '\n\\end{tabular*}\n\n'

reload(sys)
sys.setdefaultencoding('utf8')

info = info("info", 'resume.json')
education = education("education", "resume.json")
experience = experience("experience", "resume.json")
skills = skills("skills", "resume.json")

template_file = open("resume_template.tex")
template = template_file.read()
template_file.close()

out = 'mgill_resume'
try:
    out = sys.argv[1]
except:
    pass

resume = open(out + '.tex', 'w')
resume.write(template.replace('*Resume*', info + education + experience + skills))
resume.close()

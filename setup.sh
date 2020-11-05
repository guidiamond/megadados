#!/bin/sh

[ -f ".env" ] || {
    echo "You need to create .env first. Use .env.example as a template"
    exit 3
}

. ./.env

sed_cmd="s/\$DB_TASKLIST_ADMIN_PW/$DB_TASKLIST_ADMIN_PW/g;\
s/\$DB_TASKLIST_APP_PW/$DB_TASKLIST_APP_PW/g;\
"
apply_sed() {
    sed "$sed_cmd" "$1"
}

filename_clean() {
    echo "${1%_template*}${1#*_template}"
}

apply_sed_templates() {
    if [ -n "$1" ]; then
        out_folder="$1"
    else
        out_folder="."
    fi

    for file in ./*; do
        case $file in
            *_template.*)
                apply_sed "$file" > "$out_folder/$(filename_clean "$file")"
                ;;
        esac
    done
}

cd tasklist/

cd config/

apply_sed_templates

cd ../database

rm -rf init/
mkdir init

cd scripts/

for file in *; do
    case $file in
        *_template.sql)
            apply_sed "$file" > ../init/"$(filename_clean "$file")"
            ;;
        *.sql)
            cp "$file" ../init/
            ;;
    esac
done

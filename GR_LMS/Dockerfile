FROM odoo:17.0

ENV ADDON_PATH=/opt

COPY odoo.conf /etc/odoo/odoo.conf
COPY cm_addons/ ${ADDON_PATH}/cm_addons/

COPY requirements.txt requirements.txt
USER root
RUN apt-get update && apt-get install -y python3-pip && pip3 install --no-cache-dir -r requirements.txt
USER odoo

CMD ["odoo", "-d", "odoo-db"]

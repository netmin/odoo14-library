FROM odoo:14.0

USER root

ARG HOST_UID

RUN usermod -u "$HOST_UID" odoo && chown -R odoo /mnt/extra-addons

# Copyright (c) 2010-2011 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from lxml import etree
import string

import keystone.logic.types.fault as fault


class Role(object):
    def __init__(self, role_id, desc):
        self.role_id = role_id
        self.desc = desc

    @staticmethod
    def from_xml(xml_str):
        try:
            dom = etree.Element("root")
            dom.append(etree.fromstring(xml_str))
            root = dom.find("{http://docs.openstack.org/identity/api/v2.0}" \
                            "role")
            if root == None:
                raise fault.BadRequestFault("Expecting Role")
            role_id = root.get("id")
            desc = root.get("description")
            if role_id == None:
                raise fault.BadRequestFault("Expecting Role")
            return Role(role_id, desc)
        except etree.LxmlError as e:
            raise fault.BadRequestFault("Cannot parse Role", str(e))

    @staticmethod
    def from_json(json_str):
        try:
            obj = json.loads(json_str)
            if not "role" in obj:
                raise fault.BadRequestFault("Expecting Role")
            role = obj["role"]
            if not "id" in role:
                role_id = None
            else:
                role_id = role["id"]
            if role_id == None:
                raise fault.BadRequestFault("Expecting Role")
            desc = role["description"]
            return Role(role_id, desc)
        except (ValueError, TypeError) as e:
            raise fault.BadRequestFault("Cannot parse Role", str(e))

    def to_dom(self):
        dom = etree.Element("role",
                        xmlns="http://docs.openstack.org/identity/api/v2.0")
        if self.role_id:
            dom.set("id", self.role_id)
        if self.desc:
            dom.set("description", string.lower(str(self.desc)))
        return dom

    def to_xml(self):
        return etree.tostring(self.to_dom())

    def to_dict(self):
        role = {}
        if self.role_id:
            role["id"] = self.role_id
        if self.desc:
            role["description"] = self.desc
        return {'role': role}

    def to_json(self):
        return json.dumps(self.to_dict())


class Roles(object):
    "A collection of roles."

    def __init__(self, values, links):
        self.values = values
        self.links = links

    def to_xml(self):
        dom = etree.Element("roles")
        dom.set(u"xmlns", "http://docs.openstack.org/identity/api/v2.0")

        for t in self.values:
            dom.append(t.to_dom())

        for t in self.links:
            dom.append(t.to_dom())

        return etree.tostring(dom)

    def to_json(self):
        values = [t.to_dict()["role"] for t in self.values]
        links = [t.to_dict()["links"] for t in self.links]
        return json.dumps({"roles": {"values": values, "links": links}})


class RoleRef(object):
    def __init__(self, role_ref_id, role_id, tenant_id):
        self.role_ref_id = role_ref_id
        self.role_id = role_id
        self.tenant_id = tenant_id

    @staticmethod
    def from_xml(xml_str):
        try:
            dom = etree.Element("root")
            dom.append(etree.fromstring(xml_str))
            root = dom.find("{http://docs.openstack.org/identity/api/v2.0}" \
                            "roleRef")
            if root == None:
                raise fault.BadRequestFault("Expecting RoleRef")
            role_id = root.get("roleId")
            tenant_id = root.get("tenantId")
            if role_id == None:
                raise fault.BadRequestFault("Expecting Role")
            elif tenant_id == None:
                raise fault.BadRequestFault("Expecting Tenant")
            return RoleRef('', role_id, tenant_id)
        except etree.LxmlError as e:
            raise fault.BadRequestFault("Cannot parse RoleRef", str(e))

    @staticmethod
    def from_json(json_str):
        try:
            obj = json.loads(json_str)
            if not "roleRef" in obj:
                raise fault.BadRequestFault("Expecting Role Ref")
            roleRef = obj["roleRef"]
            if not "roleId" in roleRef:
                role_id = None
            else:
                role_id = roleRef["roleId"]
            if role_id == None:
                raise fault.BadRequestFault("Expecting Role")
            if not "tenantId" in roleRef:
                tenant_id = None
            else:
                tenant_id = roleRef["tenantId"]
            if tenant_id == None:
                raise fault.BadRequestFault("Expecting Tenant")
            return RoleRef('', role_id, tenant_id)
        except (ValueError, TypeError) as e:
            raise fault.BadRequestFault("Cannot parse Role", str(e))

    def to_dom(self):
        dom = etree.Element("roleRef",
                        xmlns="http://docs.openstack.org/identity/api/v2.0")
        if self.role_ref_id:
            dom.set("id", str(self.role_ref_id))
        if self.role_id:
            dom.set("roleId", self.role_id)
        if self.tenant_id:
            dom.set("tenantId", self.tenant_id)
        return dom

    def to_xml(self):
        return etree.tostring(self.to_dom())

    def to_dict(self):
        roleRef = {}
        if self.role_ref_id:
            roleRef["id"] = self.role_ref_id
        if self.role_id:
            roleRef["roleId"] = self.role_id
        if self.tenant_id:
            roleRef["tenantId"] = self.tenant_id
        return {'roleRef': roleRef}

    def to_json(self):
        return json.dumps(self.to_dict())


class RoleRefs(object):
    "A collection of role refs."

    def __init__(self, values, links):
        self.values = values
        self.links = links

    def to_xml(self):
        dom = self.to_dom()
        return etree.tostring(dom)

    def to_dom(self):
        dom = etree.Element("roleRefs")
        dom.set(u"xmlns", "http://docs.openstack.org/identity/api/v2.0")

        for t in self.values:
            dom.append(t.to_dom())

        for t in self.links:
            dom.append(t.to_dom())

        return dom

    def to_json(self):
        values = [t.to_dict()["roleRef"] for t in self.values]
        links = [t.to_dict()["links"] for t in self.links]
        return json.dumps({"roleRefs": {"values": values, "links": links}})

    def to_json_values(self):
        values = [t.to_dict()["roleRef"] for t in self.values]
        return values

# --- 0) settings
NS=default
SA=subuser
ROLE=subuser-role
BIND=subuser-binding
CTX_NAME="${SA}@k3s"
KCFG_OUT="${SA}.yaml"

# --- 1) create ServiceAccount + Role + RoleBinding
cat <<'YAML' | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: subuser
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: subuser-role
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get","list","watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: subuser-binding
  namespace: default
subjects:
- kind: ServiceAccount
  name: subuser
  namespace: default
roleRef:
  kind: Role
  name: subuser-role
  apiGroup: rbac.authorization.k8s.io
YAML

# --- 2) get endpoint and CA from cluster
SERVER=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')
CA_DATA=$(kubectl config view --raw --minify -o jsonpath='{.clusters[0].cluster.certificate-authority-data}')

# fallback 
if [ -z "$SERVER" ] || [ -z "$CA_DATA" ]; then
  SERVER=$(kubectl config view --raw -o jsonpath='{.clusters[0].cluster.server}')
  CA_DATA=$(kubectl config view --raw -o jsonpath='{.clusters[0].cluster.certificate-authority-data}')
fi

# --- 3) request ServiceAccount token
#   define token expire
if kubectl -n "$NS" create token "$SA" --duration=720h >/dev/null 2>&1; then
  TOKEN=$(kubectl -n "$NS" create token "$SA" --duration=720h)
else
  # --- 3-alt) for lagaccy
  SEC=$(kubectl -n "$NS" get sa "$SA" -o jsonpath='{.secrets[0].name}')
  TOKEN=$(kubectl -n "$NS" get secret "$SEC" -o go-template='{{.data.token | base64decode}}')
fi

# --- 4) create kubeconfig for subuser
cat > "$KCFG_OUT" <<EOF
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: ${CA_DATA}
    server: ${SERVER}
  name: k3s
contexts:
- context:
    cluster: k3s
    namespace: ${NS}
    user: ${SA}
  name: ${CTX_NAME}
current-context: ${CTX_NAME}
users:
- name: ${SA}
  user:
    token: ${TOKEN}
EOF

echo "✅ Created: ${KCFG_OUT}"
echo "Test:"
echo "KUBECONFIG=${KCFG_OUT} kubectl get pods -n ${NS}"
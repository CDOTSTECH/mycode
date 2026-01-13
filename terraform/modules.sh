
# List module block names and sources from all *.tf files
grep -R --line-number --no-color -E '^\s*module\s+"[^"]+"' -n .
grep -R --line-number --no-color -E '^\s*source\s*=\s*".+"' -n .



awk '
  /^\s*module\s*"/ {mod=$0; gsub(/^[ \t]+|[ \t]+$/, "", mod); printf FILENAME ":" FNR " " mod " "}
  /^\s*source\s*=/  {src=$0; gsub(/^[ \t]+|[ \t]+$/, "", src); print src}
' RS='\n' OFS='' $(git ls-files "*.tf" 2>/dev/null || find . -name "*.tf")
``




terraform init -upgrade >/dev/null
terraform graph -type=plan | grep -oE 'module\.[^"]+' | sort -u

Recommended workflow (accurate & repeatable)

From each root module (e.g., envs/dev, envs/prod):

terraform init
terraform-config-inspect -json . | jq (Option 2) → list declared modules
Parse .terraform.lock.hcl (Option 3) → see resolved versions


Optional: terraform graph -type=plan to validate nested usage.

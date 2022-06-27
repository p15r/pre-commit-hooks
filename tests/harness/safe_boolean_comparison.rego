package play

# run this example in playground:
# https://play.openpolicyagent.org/p/usNlKtMVlo

# input:
# {
#     "computer1": {
#         "fde_enabled": true
#     },
#     "computer2": {
#         "fde_enabled": false
#     },
#     "computer3": {},
#     "computer4": {
#         "fde_enabled": "true"
#    }
# }

is_true(b) = ret {
    is_boolean(b)
    b
    ret := b
} else = ret {
    b == "true"
    ret := true
} else = false {
    true
}

is_false(b) = ret {
    is_boolean(b)
    not b
    ret := b
} else = ret {
    b == "false"
    ret := false
} else = false {
    true
}

is_encryption_disabled_safe(computer) {
    # prevents false-positive on "computer4"
    not is_true(computer.fde_enabled)
}

is_encryption_disabled_safe(computer) {
    not computer.fde_enabled
}

deny_safe[msg] {
    some name
    computers := input
    computer := computers[name]
    
    is_encryption_disabled_safe(computer)
    
    msg := sprintf("%s has full disk encryption disabled", [name])
}

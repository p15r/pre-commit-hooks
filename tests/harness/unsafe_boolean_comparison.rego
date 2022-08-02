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

is_encryption_disabled(computer) {
    # causes a false-positive on "computer4"
    computer.fde_enabled != true
}

is_encryption_disabled(computer) {
    not computer.fde_enabled
}

deny_unsafe[msg] {
    some name
    computers := input
    computer := computers[name]

    is_encryption_disabled(computer)

    msg := sprintf("%s has full disk encryption disabled", [name])
}

dummy {
    input == true
}
dummy {
    input==true
}
dummy {
    input != true
}
dummy {
    input == false
}
dummy {
    input != false
}

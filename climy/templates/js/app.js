window.App = (function (window, document) {
  function curry(func) {
    return function curried(...args) {
      if (args.length >= func.length) {
        return func.apply(this, args);
      } else {
        return function (...args2) {
          return func.apply(this, args.concat(args2));
        };
      }
    };
  }

  function initCmdRegistry(cmd) {
    console.log("Command", cmd);
    let cmdRegistry = {
      [cmd.name]: cmd,
    };
    for (let c of cmd.subcommands) {
      cmdRegistry[c.name] = c;
    }
    return cmdRegistry;
  }

  function showFirstCmd(cmd) {
    if (cmd.subcommands.length === 0) {
      return;
    }
    let tabTrigger = document.getElementById(`${cmd.subcommands[0].name}-tab`);
    let tab = new bootstrap.Tab(tabTrigger);
    tab.show();
  }

  function setupFormSubmitListener(onSubmit) {
    const forms = document.querySelectorAll(".needs-validation");
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach(function (form) {
      form.addEventListener(
        "submit",
        (event) => {
          if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            form.classList.add("was-validated");
            return;
          }
          console.log("Reaching Here");
          onSubmit(event, form);
          form.classList.add("was-validated");
        },
        false
      );
    });
  }

  function getElemValueByType(elem, paramType) {
    switch (paramType) {
      case "string":
      case "choice":
        return elem.value != "" ? elem.value : null;
      case "int":
        return elem.value !== "" ? parseInt(elem.value) : null;
      case "float":
        return elem.value !== "" ? parseFloat(elem.value, 2) : null;
    }
    return null;
  }

  function getCmdArgument(form, param) {
    let values = [];
    const elements = form.querySelectorAll(`[data-name="${param.name}"]`);
    for (const elem of elements) {
      const value = getElemValueByType(elem, param.value_type);
      if (value !== null) {
        values.push(value);
      }
    }
    return values.length > 0
      ? {
          name: param.name,
          decl: param.decl,
          values: values,
        }
      : null;
  }

  async function setupWS(wsEventHandler) {
    return new Promise((resolve, reject) => {
      let ws = new WebSocket(`ws://${location.host}/ws`);
      ws.onopen = () => {
        resolve(ws);
      };
      ws.onerror = () => {
        reject(ws);
      };
      ws.onmessage = (event) => {
        wsEventHandler(ws, JSON.parse(event.data));
      };
    });
  }

  function getCommandHierarchy(cmd, cmdRegistry) {
    let cmdList = [cmd.name];
    while (cmd.parent_cmd !== null) {
      cmd = cmdRegistry[cmd.parent_cmd];
      cmdList.push(cmd.name);
    }
    return cmdList.reverse();
  }

  function onSubmit(ws, cmdRegistry, event, form) {
    const cmd = cmdRegistry[form.dataset.command];
    const args = [];
    for (const param of cmd.params) {
      const arg = getCmdArgument(form, param);
      if (arg !== null) {
        args.push(arg);
      }
    }
    let cmdLine = {
      commands: getCommandHierarchy(cmd, cmdRegistry),
      arguments: args,
    };
    console.log("Got CMD Line", cmdLine);
    ws.send(
      JSON.stringify({
        type: "submit",
        payload: cmdLine,
      })
    );
    event.preventDefault();
    event.stopPropagation();
  }

  function onWSEvent(ws, event) {
    console.log("Received WS Log ", event);
  }

  return {
    async init({ cmd }) {
      let _cmdRegistry = initCmdRegistry(cmd);
      showFirstCmd(cmd);
      let ws;
      try {
        ws = await setupWS(onWSEvent);
      } catch (err) {
        console.error(err);
        alert("Unable to connect websocket");
      }
      let onSubmitCurry = curry(onSubmit);
      setupFormSubmitListener(onSubmitCurry(ws, _cmdRegistry));
      document.getElementById("page-loader").classList.add("visually-hidden");
    },
  };
})(window, document);

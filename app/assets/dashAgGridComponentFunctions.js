var dagfuncs = (window.dashAgGridFunctions = window.dashAgGridFunctions || {});

var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.versionChangeCellRendererSelector = (params) => {
    const fieldGenerator = (icon, iconColor) => React.createElement('div',
        {
        style: {
            gap: '8px',
            paddingTop:'5px'
        }
    },
    [
        React.createElement(
            window.dash_iconify.DashIconify,
            {
                icon: icon,
                color: iconColor,
                height: '20px',
                style: {},
            },
        ),
    ]);


    if (params.value === 'updated') {
        return fieldGenerator('ph:tilde-fill', '#D19E21');
    }
    if (params.value === 'deleted') {
        return fieldGenerator('ph:minus-fill', '#bc4429');
    }
    if (params.value === 'inserted') {
        return fieldGenerator('ph:plus-fill', '#6d8e51');
    }
    return params.value;
}

dagcomponentfuncs.DMC_Button = function (props) {
    const {setData, data} = props;

    function onClick() {
        setData();
    }
    let leftIcon, rightIcon;
    if (props.leftIcon) {
        leftIcon = React.createElement(window.dash_iconify.DashIconify, {
            icon: props.leftIcon,
        });
    }
    if (props.rightIcon) {
        rightIcon = React.createElement(window.dash_iconify.DashIconify, {
            icon: props.rightIcon,
        });
    }
    return React.createElement(
        window.dash_mantine_components.Button,
        {
            onClick,
            variant: props.variant,
            color: props.color,
            leftIcon,
            rightIcon,
            radius: props.radius,
            style: {
                margin: props.margin,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
            },
        },
        props.value
    );
};

// custom component to display boolean data as a checkbox
dagcomponentfuncs.Checkbox = function (props) {
    const { setData, data } = props;
    function onClick() {
        if (!('checked' in event.target)) {
            const checked = !event.target.children[0].checked;
            const colId = props.column.colId;
            props.node.setDataValue(colId, checked);
        }
    }
    function checkedHandler() {
        // update grid data
        const checked = event.target.checked;
        const colId = props.column.colId;
        props.node.setDataValue(colId, checked);
        // update cellRendererData prop so it can be used to trigger a callback
        setData(checked);
    }
    return React.createElement(
        'div',
        { onClick: onClick },
        React.createElement('input', {
            type: 'checkbox',
            checked: props.value,
            onChange: checkedHandler,
            style: { cursor: 'pointer', 'accentColor': '#1876AD'},
        })
    );
};

dagfuncs.getOptions = function(options) {

    return {
        values: options,
        allowTyping: true,
        filterList: true,
        highlightMatch: true,
        valueListMaxHeight: 220
    }
}

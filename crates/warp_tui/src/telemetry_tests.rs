use warp_core::telemetry::TelemetryEvent as _;

use super::*;

#[test]
fn conversation_menu_events_use_tui_native_names() {
    let opened = TuiConversationMenuTelemetryEvent::Opened;
    let selected = TuiConversationMenuTelemetryEvent::ItemSelected;

    assert_eq!(TelemetryEvent::name(&opened), "TUI.ConversationMenu.Opened");
    assert_eq!(
        TelemetryEvent::name(&selected),
        "TUI.ConversationMenu.ItemSelected"
    );
    assert_eq!(opened.payload(), None);
    assert_eq!(selected.payload(), None);
}

#[test]
fn conversation_restore_payload_is_low_cardinality_and_non_ugc() {
    let event = TuiConversationRestoreTelemetryEvent {
        state: TuiConversationRestoreTelemetryState::Failed,
        target: TuiConversationRestoreTelemetryTarget::Server,
    };

    assert_eq!(TelemetryEvent::name(&event), "TUI.ConversationRestore");
    assert_eq!(
        event.payload(),
        Some(json!({
            "state": "failed",
            "target": "server",
        }))
    );
    assert!(!event.contains_ugc());
}

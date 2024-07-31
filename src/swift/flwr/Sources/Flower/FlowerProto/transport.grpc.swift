//
// DO NOT EDIT.
// swift-format-ignore-file
//
// Generated by the protocol buffer compiler.
// Source: flwr/proto/transport.proto
//
import GRPC
import NIO
import NIOConcurrencyHelpers
import SwiftProtobuf


/// Usage: instantiate `Flwr_Proto_FlowerServiceClient`, then call methods of this protocol to make API calls.
internal protocol Flwr_Proto_FlowerServiceClientProtocol: GRPCClient {
  var serviceName: String { get }
  var interceptors: Flwr_Proto_FlowerServiceClientInterceptorFactoryProtocol? { get }

  func join(
    callOptions: CallOptions?,
    handler: @escaping (Flwr_Proto_ServerMessage) -> Void
  ) -> BidirectionalStreamingCall<Flwr_Proto_ClientMessage, Flwr_Proto_ServerMessage>
}

extension Flwr_Proto_FlowerServiceClientProtocol {
  internal var serviceName: String {
    return "flwr.proto.FlowerService"
  }

  /// Bidirectional streaming call to Join
  ///
  /// Callers should use the `send` method on the returned object to send messages
  /// to the server. The caller should send an `.end` after the final message has been sent.
  ///
  /// - Parameters:
  ///   - callOptions: Call options.
  ///   - handler: A closure called when each response is received from the server.
  /// - Returns: A `ClientStreamingCall` with futures for the metadata and status.
  internal func join(
    callOptions: CallOptions? = nil,
    handler: @escaping (Flwr_Proto_ServerMessage) -> Void
  ) -> BidirectionalStreamingCall<Flwr_Proto_ClientMessage, Flwr_Proto_ServerMessage> {
    return self.makeBidirectionalStreamingCall(
      path: Flwr_Proto_FlowerServiceClientMetadata.Methods.join.path,
      callOptions: callOptions ?? self.defaultCallOptions,
      interceptors: self.interceptors?.makeJoinInterceptors() ?? [],
      handler: handler
    )
  }
}

@available(*, deprecated)
extension Flwr_Proto_FlowerServiceClient: @unchecked Sendable {}

@available(*, deprecated, renamed: "Flwr_Proto_FlowerServiceNIOClient")
internal final class Flwr_Proto_FlowerServiceClient: Flwr_Proto_FlowerServiceClientProtocol {
  private let lock = Lock()
  private var _defaultCallOptions: CallOptions
  private var _interceptors: Flwr_Proto_FlowerServiceClientInterceptorFactoryProtocol?
  internal let channel: GRPCChannel
  internal var defaultCallOptions: CallOptions {
    get { self.lock.withLock { return self._defaultCallOptions } }
    set { self.lock.withLockVoid { self._defaultCallOptions = newValue } }
  }
  internal var interceptors: Flwr_Proto_FlowerServiceClientInterceptorFactoryProtocol? {
    get { self.lock.withLock { return self._interceptors } }
    set { self.lock.withLockVoid { self._interceptors = newValue } }
  }

  /// Creates a client for the flwr.proto.FlowerService service.
  ///
  /// - Parameters:
  ///   - channel: `GRPCChannel` to the service host.
  ///   - defaultCallOptions: Options to use for each service call if the user doesn't provide them.
  ///   - interceptors: A factory providing interceptors for each RPC.
  internal init(
    channel: GRPCChannel,
    defaultCallOptions: CallOptions = CallOptions(),
    interceptors: Flwr_Proto_FlowerServiceClientInterceptorFactoryProtocol? = nil
  ) {
    self.channel = channel
    self._defaultCallOptions = defaultCallOptions
    self._interceptors = interceptors
  }
}

internal struct Flwr_Proto_FlowerServiceNIOClient: Flwr_Proto_FlowerServiceClientProtocol {
  internal var channel: GRPCChannel
  internal var defaultCallOptions: CallOptions
  internal var interceptors: Flwr_Proto_FlowerServiceClientInterceptorFactoryProtocol?

  /// Creates a client for the flwr.proto.FlowerService service.
  ///
  /// - Parameters:
  ///   - channel: `GRPCChannel` to the service host.
  ///   - defaultCallOptions: Options to use for each service call if the user doesn't provide them.
  ///   - interceptors: A factory providing interceptors for each RPC.
  internal init(
    channel: GRPCChannel,
    defaultCallOptions: CallOptions = CallOptions(),
    interceptors: Flwr_Proto_FlowerServiceClientInterceptorFactoryProtocol? = nil
  ) {
    self.channel = channel
    self.defaultCallOptions = defaultCallOptions
    self.interceptors = interceptors
  }
}

@available(macOS 10.15, iOS 13, tvOS 13, watchOS 6, *)
internal protocol Flwr_Proto_FlowerServiceAsyncClientProtocol: GRPCClient {
  static var serviceDescriptor: GRPCServiceDescriptor { get }
  var interceptors: Flwr_Proto_FlowerServiceClientInterceptorFactoryProtocol? { get }

  func makeJoinCall(
    callOptions: CallOptions?
  ) -> GRPCAsyncBidirectionalStreamingCall<Flwr_Proto_ClientMessage, Flwr_Proto_ServerMessage>
}

@available(macOS 10.15, iOS 13, tvOS 13, watchOS 6, *)
extension Flwr_Proto_FlowerServiceAsyncClientProtocol {
  internal static var serviceDescriptor: GRPCServiceDescriptor {
    return Flwr_Proto_FlowerServiceClientMetadata.serviceDescriptor
  }

  internal var interceptors: Flwr_Proto_FlowerServiceClientInterceptorFactoryProtocol? {
    return nil
  }

  internal func makeJoinCall(
    callOptions: CallOptions? = nil
  ) -> GRPCAsyncBidirectionalStreamingCall<Flwr_Proto_ClientMessage, Flwr_Proto_ServerMessage> {
    return self.makeAsyncBidirectionalStreamingCall(
      path: Flwr_Proto_FlowerServiceClientMetadata.Methods.join.path,
      callOptions: callOptions ?? self.defaultCallOptions,
      interceptors: self.interceptors?.makeJoinInterceptors() ?? []
    )
  }
}

@available(macOS 10.15, iOS 13, tvOS 13, watchOS 6, *)
extension Flwr_Proto_FlowerServiceAsyncClientProtocol {
  internal func join<RequestStream>(
    _ requests: RequestStream,
    callOptions: CallOptions? = nil
  ) -> GRPCAsyncResponseStream<Flwr_Proto_ServerMessage> where RequestStream: Sequence, RequestStream.Element == Flwr_Proto_ClientMessage {
    return self.performAsyncBidirectionalStreamingCall(
      path: Flwr_Proto_FlowerServiceClientMetadata.Methods.join.path,
      requests: requests,
      callOptions: callOptions ?? self.defaultCallOptions,
      interceptors: self.interceptors?.makeJoinInterceptors() ?? []
    )
  }

  internal func join<RequestStream>(
    _ requests: RequestStream,
    callOptions: CallOptions? = nil
  ) -> GRPCAsyncResponseStream<Flwr_Proto_ServerMessage> where RequestStream: AsyncSequence & Sendable, RequestStream.Element == Flwr_Proto_ClientMessage {
    return self.performAsyncBidirectionalStreamingCall(
      path: Flwr_Proto_FlowerServiceClientMetadata.Methods.join.path,
      requests: requests,
      callOptions: callOptions ?? self.defaultCallOptions,
      interceptors: self.interceptors?.makeJoinInterceptors() ?? []
    )
  }
}

@available(macOS 10.15, iOS 13, tvOS 13, watchOS 6, *)
internal struct Flwr_Proto_FlowerServiceAsyncClient: Flwr_Proto_FlowerServiceAsyncClientProtocol {
  internal var channel: GRPCChannel
  internal var defaultCallOptions: CallOptions
  internal var interceptors: Flwr_Proto_FlowerServiceClientInterceptorFactoryProtocol?

  internal init(
    channel: GRPCChannel,
    defaultCallOptions: CallOptions = CallOptions(),
    interceptors: Flwr_Proto_FlowerServiceClientInterceptorFactoryProtocol? = nil
  ) {
    self.channel = channel
    self.defaultCallOptions = defaultCallOptions
    self.interceptors = interceptors
  }
}

internal protocol Flwr_Proto_FlowerServiceClientInterceptorFactoryProtocol: Sendable {

  /// - Returns: Interceptors to use when invoking 'join'.
  func makeJoinInterceptors() -> [ClientInterceptor<Flwr_Proto_ClientMessage, Flwr_Proto_ServerMessage>]
}

internal enum Flwr_Proto_FlowerServiceClientMetadata {
  internal static let serviceDescriptor = GRPCServiceDescriptor(
    name: "FlowerService",
    fullName: "flwr.proto.FlowerService",
    methods: [
      Flwr_Proto_FlowerServiceClientMetadata.Methods.join,
    ]
  )

  internal enum Methods {
    internal static let join = GRPCMethodDescriptor(
      name: "Join",
      path: "/flwr.proto.FlowerService/Join",
      type: GRPCCallType.bidirectionalStreaming
    )
  }
}

/// To build a server, implement a class that conforms to this protocol.
internal protocol Flwr_Proto_FlowerServiceProvider: CallHandlerProvider {
  var interceptors: Flwr_Proto_FlowerServiceServerInterceptorFactoryProtocol? { get }

  func join(context: StreamingResponseCallContext<Flwr_Proto_ServerMessage>) -> EventLoopFuture<(StreamEvent<Flwr_Proto_ClientMessage>) -> Void>
}

extension Flwr_Proto_FlowerServiceProvider {
  internal var serviceName: Substring {
    return Flwr_Proto_FlowerServiceServerMetadata.serviceDescriptor.fullName[...]
  }

  /// Determines, calls and returns the appropriate request handler, depending on the request's method.
  /// Returns nil for methods not handled by this service.
  internal func handle(
    method name: Substring,
    context: CallHandlerContext
  ) -> GRPCServerHandlerProtocol? {
    switch name {
    case "Join":
      return BidirectionalStreamingServerHandler(
        context: context,
        requestDeserializer: ProtobufDeserializer<Flwr_Proto_ClientMessage>(),
        responseSerializer: ProtobufSerializer<Flwr_Proto_ServerMessage>(),
        interceptors: self.interceptors?.makeJoinInterceptors() ?? [],
        observerFactory: self.join(context:)
      )

    default:
      return nil
    }
  }
}

/// To implement a server, implement an object which conforms to this protocol.
@available(macOS 10.15, iOS 13, tvOS 13, watchOS 6, *)
internal protocol Flwr_Proto_FlowerServiceAsyncProvider: CallHandlerProvider, Sendable {
  static var serviceDescriptor: GRPCServiceDescriptor { get }
  var interceptors: Flwr_Proto_FlowerServiceServerInterceptorFactoryProtocol? { get }

  func join(
    requestStream: GRPCAsyncRequestStream<Flwr_Proto_ClientMessage>,
    responseStream: GRPCAsyncResponseStreamWriter<Flwr_Proto_ServerMessage>,
    context: GRPCAsyncServerCallContext
  ) async throws
}

@available(macOS 10.15, iOS 13, tvOS 13, watchOS 6, *)
extension Flwr_Proto_FlowerServiceAsyncProvider {
  internal static var serviceDescriptor: GRPCServiceDescriptor {
    return Flwr_Proto_FlowerServiceServerMetadata.serviceDescriptor
  }

  internal var serviceName: Substring {
    return Flwr_Proto_FlowerServiceServerMetadata.serviceDescriptor.fullName[...]
  }

  internal var interceptors: Flwr_Proto_FlowerServiceServerInterceptorFactoryProtocol? {
    return nil
  }

  internal func handle(
    method name: Substring,
    context: CallHandlerContext
  ) -> GRPCServerHandlerProtocol? {
    switch name {
    case "Join":
      return GRPCAsyncServerHandler(
        context: context,
        requestDeserializer: ProtobufDeserializer<Flwr_Proto_ClientMessage>(),
        responseSerializer: ProtobufSerializer<Flwr_Proto_ServerMessage>(),
        interceptors: self.interceptors?.makeJoinInterceptors() ?? [],
        wrapping: { try await self.join(requestStream: $0, responseStream: $1, context: $2) }
      )

    default:
      return nil
    }
  }
}

internal protocol Flwr_Proto_FlowerServiceServerInterceptorFactoryProtocol: Sendable {

  /// - Returns: Interceptors to use when handling 'join'.
  ///   Defaults to calling `self.makeInterceptors()`.
  func makeJoinInterceptors() -> [ServerInterceptor<Flwr_Proto_ClientMessage, Flwr_Proto_ServerMessage>]
}

internal enum Flwr_Proto_FlowerServiceServerMetadata {
  internal static let serviceDescriptor = GRPCServiceDescriptor(
    name: "FlowerService",
    fullName: "flwr.proto.FlowerService",
    methods: [
      Flwr_Proto_FlowerServiceServerMetadata.Methods.join,
    ]
  )

  internal enum Methods {
    internal static let join = GRPCMethodDescriptor(
      name: "Join",
      path: "/flwr.proto.FlowerService/Join",
      type: GRPCCallType.bidirectionalStreaming
    )
  }
}
